"""
AI Code Intelligence Engine - Utils Module
Logging, configuration, and environment path management.
"""

from .logger import logger
from .config import (
    BASE_DIR,
    DATA_DIR,
    INDEX_DIR,
    EMBEDDING_MODEL_NAME,
    SUPPORTED_EXTENSIONS,
    FAISS_INDEX_FILE,
    METADATA_FILE,
)

__all__ = [
    "logger",
    "BASE_DIR",
    "DATA_DIR",
    "INDEX_DIR",
    "EMBEDDING_MODEL_NAME",
    "SUPPORTED_EXTENSIONS",
    "FAISS_INDEX_FILE",
    "METADATA_FILE",
]
