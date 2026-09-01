import os
import shutil
import stat
import subprocess
import tempfile
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

class GitHubIndexer:
    def __init__(self, embedding_gen: EmbeddingGenerator, vector_store: FaissIndex):
        self.embedding_gen = embedding_gen
        self.vector_store = vector_store

    def index_repo(self, repo_url: str):
        if not repo_url or not repo_url.strip():
            raise ValueError("Repository URL cannot be empty")

        clean_url = repo_url.strip()
        temp_dir = tempfile.mkdtemp(prefix="repo_ingest_")
        try:
            logger.info(f"Cloning repository {clean_url} to sandbox {temp_dir}...")
            # Fast shallow single-branch clone
            proc = subprocess.run(
                [
                    "git", "clone",
                    "--depth", "1",
                    "--single-branch",
                    "--no-tags",
                    "-q",
                    clean_url,
                    temp_dir
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if proc.returncode != 0:
                logger.error(f"Git clone failed for {clean_url}: {proc.stderr}")
                raise RuntimeError(f"Git clone failed: {proc.stderr.strip() or 'Unknown error'}")

            # Immediately purge .git directory to minimize disk and avoid lockfiles
            git_dir = os.path.join(temp_dir, ".git")
            if os.path.exists(git_dir):
                shutil.rmtree(git_dir, onerror=_remove_readonly)
            
            scanner = RepoScanner(temp_dir)
            files = scanner.scan()
            
            # Scan top 20 application source files for rapid cloud response
            if len(files) > 20:
                files = files[:20]
            
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
                # Cap snippets to 35 on remote cloud ingestion to guarantee response in < 2 seconds
                MAX_INGEST_SNIPPETS = 35
                if len(all_snippets) > MAX_INGEST_SNIPPETS:
                    logger.info(f"Limiting remote indexing to top {MAX_INGEST_SNIPPETS} entities for instant response.")
                    all_snippets = all_snippets[:MAX_INGEST_SNIPPETS]
                    all_metadata = all_metadata[:MAX_INGEST_SNIPPETS]

                embeddings = self.embedding_gen.generate(all_snippets)
                self.vector_store.add_embeddings(embeddings, all_metadata)
                self.vector_store.save()
                logger.info(f"Successfully indexed GitHub repository: {clean_url} ({len(files)} files, {len(all_snippets)} snippets)")
                return {"status": "success", "repo_url": clean_url, "indexed_files": len(files), "snippets": len(all_snippets)}
            
            logger.warning(f"No supported code files found in repository: {clean_url}")
            return {"status": "no_code_found", "repo_url": clean_url, "indexed_files": 0, "snippets": 0}
            
        except subprocess.TimeoutExpired:
            logger.error(f"Git clone timed out for {clean_url}")
            raise RuntimeError("Git clone operation timed out after 30s.")
        except Exception as e:
            logger.error(f"Error indexing repository {clean_url}: {e}")
            raise
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, onerror=_remove_readonly)
            logger.info(f"Cleaned up temporary directory {temp_dir}")
