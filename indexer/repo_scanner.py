import os
from typing import List
from indexer.language_detector import LanguageDetector
from utils.logger import logger

IGNORED_DIRS = {
    ".git", ".github", ".venv", "venv", "env", "ENV",
    "node_modules", "build", "dist", "__pycache__",
    ".pytest_cache", ".docs", "docs", "site-packages",
    "vendor", ".tox", "htmlcov"
}

class RepoScanner:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def scan(self) -> List[str]:
        logger.info(f"Scanning directory: {self.root_dir}")
        supported_files = []
        for root, dirs, files in os.walk(self.root_dir):
            # Prune ignored directories in-place
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]
            
            for file in files:
                file_path = os.path.join(root, file)
                if LanguageDetector.is_supported(file_path):
                    supported_files.append(file_path)
        
        logger.info(f"Found {len(supported_files)} supported files.")
        return supported_files
