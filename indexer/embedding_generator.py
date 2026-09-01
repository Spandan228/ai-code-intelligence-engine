import os
import gc
from typing import List, Optional
import numpy as np
from utils.config import EMBEDDING_MODEL_NAME
from utils.logger import logger

# Set thread limits before importing torch / sentence_transformers to minimize memory overhead
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class EmbeddingGenerator:
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}...")
            try:
                import torch
                torch.set_num_threads(1)
                if hasattr(torch, "set_num_interop_threads"):
                    try:
                        torch.set_num_interop_threads(1)
                    except RuntimeError:
                        pass
            except ImportError:
                pass

            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            logger.info(f"Successfully loaded {self.model_name} in low-memory mode.")
        return self._model

    def generate(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 384), dtype=np.float32)
        
        model = self.model
        all_embeddings = []
        chunk_size = 16
        
        for i in range(0, len(texts), chunk_size):
            chunk = texts[i : i + chunk_size]
            try:
                import torch
                with torch.inference_mode():
                    emb = model.encode(chunk, batch_size=chunk_size, show_progress_bar=False, normalize_embeddings=True)
            except Exception:
                emb = model.encode(chunk, batch_size=chunk_size, show_progress_bar=False, normalize_embeddings=True)
            all_embeddings.append(emb)
            gc.collect()
            
        return np.vstack(all_embeddings).astype(np.float32)
