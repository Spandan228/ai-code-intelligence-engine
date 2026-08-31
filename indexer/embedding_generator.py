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
            logger.info(f"Lazily loading embedding model: {self.model_name}...")
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
            return np.array([])
        
        try:
            import torch
            with torch.inference_mode():
                embeddings = self.model.encode(texts, batch_size=8, show_progress_bar=False, normalize_embeddings=True)
        except Exception:
            embeddings = self.model.encode(texts, batch_size=8, show_progress_bar=False, normalize_embeddings=True)
            
        gc.collect()
        return np.array(embeddings, dtype=np.float32)
