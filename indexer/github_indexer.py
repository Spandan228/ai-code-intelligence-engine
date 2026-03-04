import os
import shutil
import tempfile
from git import Repo
from indexer.repo_scanner import RepoScanner
from indexer.code_parser import CodeParserOrchestrator
from indexer.embedding_generator import EmbeddingGenerator
from vector_store.faiss_index import FaissIndex
from utils.logger import logger

class GitHubIndexer:
    def __init__(self, embedding_gen: EmbeddingGenerator, vector_store: FaissIndex):
        self.embedding_gen = embedding_gen
        self.vector_store = vector_store

    def index_repo(self, repo_url: str):
        temp_dir = tempfile.mkdtemp()
        try:
            logger.info(f"Cloning repository {repo_url} to {temp_dir}...")
            Repo.clone_from(repo_url, temp_dir)
            
            scanner = RepoScanner(temp_dir)
            files = scanner.scan()
            
            orchestrator = CodeParserOrchestrator()
            all_metadata = []
            all_snippets = []
            
            for file_path in files:
                metadata_list = orchestrator.parse_file(file_path)
                for meta in metadata_list:
                    # Adjust file path to be relative to the temp_dir or just the filename for display
                    meta["file_path"] = os.path.relpath(meta["file_path"], temp_dir)
                    all_metadata.append(meta)
                    all_snippets.append(meta["code_snippet"])
            
            if all_snippets:
                embeddings = self.embedding_gen.generate(all_snippets)
                self.vector_store.add_embeddings(embeddings, all_metadata)
                self.vector_store.save()
            
            logger.info(f"Successfully indexed GitHub repository: {repo_url}")
            
        finally:
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary directory {temp_dir}")
