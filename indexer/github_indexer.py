import os
import shutil
import stat
import tempfile
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

class GitHubIndexer:
    def __init__(self, embedding_gen: EmbeddingGenerator, vector_store: FaissIndex):
        self.embedding_gen = embedding_gen
        self.vector_store = vector_store

    def index_repo(self, repo_url: str):
        if not repo_url or not repo_url.strip():
            raise ValueError("Repository URL cannot be empty")

        temp_dir = tempfile.mkdtemp(prefix="repo_clone_")
        try:
            logger.info(f"Cloning repository {repo_url} to {temp_dir}...")
            Repo.clone_from(repo_url.strip(), temp_dir, depth=1)
            
            scanner = RepoScanner(temp_dir)
            files = scanner.scan()
            
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
                embeddings = self.embedding_gen.generate(all_snippets)
                self.vector_store.add_embeddings(embeddings, all_metadata)
                self.vector_store.save()
                logger.info(f"Successfully indexed GitHub repository: {repo_url} ({len(files)} files, {len(all_snippets)} snippets)")
                return {"status": "success", "indexed_files": len(files), "snippets": len(all_snippets)}
            
            logger.warning(f"No supported code files found in repository: {repo_url}")
            return {"status": "no_code_found", "indexed_files": 0, "snippets": 0}
            
        except GitCommandError as e:
            logger.error(f"Git clone failed for {repo_url}: {e}")
            raise RuntimeError(f"Git clone failed: {e.stderr if hasattr(e, 'stderr') else str(e)}")
        except Exception as e:
            logger.error(f"Error indexing repository {repo_url}: {e}")
            raise
        finally:
            shutil.rmtree(temp_dir, onerror=_remove_readonly)
            logger.info(f"Cleaned up temporary directory {temp_dir}")
