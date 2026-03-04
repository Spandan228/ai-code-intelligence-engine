import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from indexer.repo_scanner import RepoScanner
from indexer.code_parser import CodeParserOrchestrator
from indexer.embedding_generator import EmbeddingGenerator
from vector_store.faiss_index import FaissIndex
from utils.logger import logger

def main():
    if len(sys.argv) < 2:
        print("Usage: python index_repository.py <repository_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    if not os.path.exists(repo_path):
        logger.error(f"Path does not exist: {repo_path}")
        sys.exit(1)

    # Initialize components
    embedding_gen = EmbeddingGenerator()
    vector_store = FaissIndex()
    orchestrator = CodeParserOrchestrator()
    scanner = RepoScanner(repo_path)

    # Scan and Parse
    files = scanner.scan()
    all_metadata = []
    all_snippets = []

    logger.info("Parsing files...")
    for f in files:
        meta_list = orchestrator.parse_file(f)
        for meta in meta_list:
            # Shorten paths for the index
            meta["file_path"] = os.path.relpath(meta["file_path"], repo_path)
            all_metadata.append(meta)
            all_snippets.append(meta["code_snippet"])

    # Generate Embeddings and Save
    if all_snippets:
        logger.info(f"Generating embeddings for {len(all_snippets)} snippets...")
        embeddings = embedding_gen.generate(all_snippets)
        vector_store.add_embeddings(embeddings, all_metadata)
        vector_store.save()
        logger.info("Indexing complete!")
    else:
        logger.warning("No code snippets found to index.")

if __name__ == "__main__":
    main()
