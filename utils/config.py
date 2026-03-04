import os
from pathlib import Path

# Project Roots
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = DATA_DIR / "indices"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
INDEX_DIR.mkdir(exist_ok=True)

# Model Settings
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Supported Languages
SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp"
}

# Vector Store Settings
FAISS_INDEX_FILE = INDEX_DIR / "code_embeddings.index"
METADATA_FILE = INDEX_DIR / "code_metadata.pkl"
