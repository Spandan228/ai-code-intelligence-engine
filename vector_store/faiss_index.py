import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Tuple
from utils.config import FAISS_INDEX_FILE, METADATA_FILE
from utils.logger import logger

class FaissIndex:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product for normalized cosine similarity
        self.metadata: List[Dict[str, Any]] = []

    def add_embeddings(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        if embeddings is None or embeddings.shape[0] == 0:
            return
        
        # Ensure contiguous float32 array for safe FAISS C++ bindings
        embeddings = np.ascontiguousarray(embeddings, dtype=np.float32)
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        self.metadata.extend(metadata)
        logger.info(f"Added {embeddings.shape[0]} embeddings to FAISS index.")

    def save(self):
        os.makedirs(os.path.dirname(str(FAISS_INDEX_FILE)), exist_ok=True)
        os.makedirs(os.path.dirname(str(METADATA_FILE)), exist_ok=True)
        faiss.write_index(self.index, str(FAISS_INDEX_FILE))
        with open(METADATA_FILE, "wb") as f:
            pickle.dump(self.metadata, f)
        logger.info(f"Saved FAISS index to {FAISS_INDEX_FILE}")

    def load(self):
        if os.path.exists(FAISS_INDEX_FILE) and os.path.exists(METADATA_FILE):
            self.index = faiss.read_index(str(FAISS_INDEX_FILE))
            with open(METADATA_FILE, "rb") as f:
                self.metadata = pickle.load(f)
            logger.info(f"Loaded FAISS index from {FAISS_INDEX_FILE}")
        else:
            logger.warning("FAISS index or metadata file not found. Starting with empty index.")

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        if self.index.ntotal == 0 or query_embedding is None or len(query_embedding) == 0:
            return []
        
        query_embedding = np.ascontiguousarray(query_embedding, dtype=np.float32)
        faiss.normalize_L2(query_embedding)
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append((self.metadata[idx], float(distances[0][i])))
        
        return results

    def reset(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.metadata = []
        if os.path.exists(FAISS_INDEX_FILE):
            try:
                os.remove(FAISS_INDEX_FILE)
            except Exception:
                pass
        if os.path.exists(METADATA_FILE):
            try:
                os.remove(METADATA_FILE)
            except Exception:
                pass
        logger.info("Reset FAISS index and metadata.")
