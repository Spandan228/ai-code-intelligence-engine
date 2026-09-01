import os
import re
import io
import shutil
import stat
import tempfile
import urllib.request
import zipfile
from git import Repo
from git.exc import GitCommandError
from indexer.repo_scanner import RepoScanner
from indexer.code_parser import CodeParserOrchestrator
from indexer.embedding_generator import EmbeddingGenerator
from vector_store.faiss_index import FaissIndex
from utils.logger import logger

def _remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def _fetch_github_archive(repo_url: str, dest_dir: str) -> bool:
    """
    Downloads repository zip archive directly via HTTPS in ~1 second,
    bypassing heavy git clone subprocesses.
    """
    match = re.search(r"github\.com/([^/]+)/([^/\.]+)", repo_url)
    if not match:
        return False
    
    owner, repo = match.group(1), match.group(2)
    branches = ["main", "master", "develop"]
    
    for branch in branches:
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
        try:
            req = urllib.request.Request(
                zip_url,
                headers={"User-Agent": "AI-Code-Intelligence-Engine/2.0"}
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    zip_data = resp.read()
                    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
                        z.extractall(dest_dir)
                    logger.info(f"Successfully downloaded and extracted GitHub archive for {owner}/{repo} ({branch})")
                    return True
        except Exception as e:
            logger.debug(f"Archive fetch branch '{branch}' failed: {e}")
            continue
            
    return False

class GitHubIndexer:
    def __init__(self, embedding_gen: EmbeddingGenerator, vector_store: FaissIndex):
        self.embedding_gen = embedding_gen
        self.vector_store = vector_store

    def index_repo(self, repo_url: str):
        if not repo_url or not repo_url.strip():
            raise ValueError("Repository URL cannot be empty")

        temp_dir = tempfile.mkdtemp(prefix="repo_ingest_")
        try:
            logger.info(f"Ingesting repository {repo_url}...")
            # 1. Try ultra-fast direct archive extraction (sub-second)
            downloaded = _fetch_github_archive(repo_url.strip(), temp_dir)
            
            # 2. Fallback to Git shallow clone if archive download unavailable
            if not downloaded:
                logger.info(f"Falling back to git shallow clone for {repo_url}...")
                Repo.clone_from(
                    repo_url.strip(),
                    temp_dir,
                    depth=1,
                    single_branch=True,
                    no_tags=True,
                )
            
            # Purge .git directory if present
            git_dir = os.path.join(temp_dir, ".git")
            if os.path.exists(git_dir):
                shutil.rmtree(git_dir, onerror=_remove_readonly)
            
            scanner = RepoScanner(temp_dir)
            files = scanner.scan()
            
            # Scan top 35 application source files
            if len(files) > 35:
                files = files[:35]
            
            orchestrator = CodeParserOrchestrator()
            all_metadata = []
            all_snippets = []
            
            for file_path in files:
                metadata_list = orchestrator.parse_file(file_path)
                for meta in metadata_list:
                    meta["file_path"] = os.path.relpath(meta["file_path"], temp_dir).replace("\\", "/")
                    all_metadata.append(meta)
                    all_snippets.append(meta["code_snippet"])
            
            if all_snippets:
                # Cap snippets to 75 on remote cloud ingestion to guarantee sub-3s response
                MAX_INGEST_SNIPPETS = 75
                if len(all_snippets) > MAX_INGEST_SNIPPETS:
                    logger.info(f"Limiting remote indexing to top {MAX_INGEST_SNIPPETS} entities for instant response.")
                    all_snippets = all_snippets[:MAX_INGEST_SNIPPETS]
                    all_metadata = all_metadata[:MAX_INGEST_SNIPPETS]

                embeddings = self.embedding_gen.generate(all_snippets)
                self.vector_store.add_embeddings(embeddings, all_metadata)
                self.vector_store.save()
                logger.info(f"Successfully indexed GitHub repository: {repo_url} ({len(files)} files, {len(all_snippets)} snippets)")
                return {"status": "success", "repo_url": repo_url, "indexed_files": len(files), "snippets": len(all_snippets)}
            
            logger.warning(f"No supported code files found in repository: {repo_url}")
            return {"status": "no_code_found", "repo_url": repo_url, "indexed_files": 0, "snippets": 0}
            
        except GitCommandError as e:
            logger.error(f"Git clone failed for {repo_url}: {e}")
            raise RuntimeError(f"Git clone failed: {e.stderr if hasattr(e, 'stderr') else str(e)}")
        except Exception as e:
            logger.error(f"Error indexing repository {repo_url}: {e}")
            raise
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, onerror=_remove_readonly)
            logger.info(f"Cleaned up temporary directory {temp_dir}")
