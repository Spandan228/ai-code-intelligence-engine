import os
from typing import List
from indexer.language_detector import LanguageDetector
from tqdm import tqdm
from utils.logger import logger

class RepoScanner:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def scan(self) -> List[str]:
        logger.info(f"Scanning directory: {self.root_dir}")
        supported_files = []
        for root, _, files in os.walk(self.root_dir):
            # Skip hidden directories like .git
            if "/." in root or "\\." in root:
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                if LanguageDetector.is_supported(file_path):
                    supported_files.append(file_path)
        
        logger.info(f"Found {len(supported_files)} supported files.")
        return supported_files
