import os
from utils.config import SUPPORTED_EXTENSIONS

class LanguageDetector:
    @staticmethod
    def get_language(file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        return SUPPORTED_EXTENSIONS.get(ext.lower(), "unknown")

    @staticmethod
    def is_supported(file_path: str) -> bool:
        _, ext = os.path.splitext(file_path)
        return ext.lower() in SUPPORTED_EXTENSIONS
