import os
import gc
from typing import List, Optional
import numpy as np
from utils.config import EMBEDDING_MODEL_NAME
from utils.logger import logger

class EmbeddingGenerator:
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self._model = None
        self._device = None

    @property
    def device(self) -> str:
        if self._device is None:
            try:
                import torch
                if torch.cuda.is_available():
                    self._device = "cuda"
                elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    self._device = "mps"
                else:
                    self._device = "cpu"
            except Exception:
                self._device = "cpu"
        return self._device

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name} on device [{self.device.upper()}]...")
            from sentence_transformers import SentenceTransformer
            base_model = SentenceTransformer(self.model_name, device=self.device)
            
            if self.device == "cpu":
                try:
                    import torch
                    if len(base_model) > 0 and hasattr(base_model[0], "auto_model"):
                        base_model[0].auto_model = torch.quantization.quantize_dynamic(
                            base_model[0].auto_model, {torch.nn.Linear}, dtype=torch.qint8
                        )
                        logger.info("Successfully applied 8-bit dynamic quantization for CPU acceleration.")
                except Exception as q_err:
                    logger.debug(f"Quantization notice: {q_err}")

            self._model = base_model
            logger.info(f"Successfully loaded {self.model_name} on {self.device.upper()}.")
        return self._model

    def generate(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 384), dtype=np.float32)
        
        model = self.model
        batch_size = 32 if self.device != "cpu" else 16
        try:
            import torch
            with torch.inference_mode():
                embeddings = model.encode(
                    texts,
                    batch_size=batch_size,
                    show_progress_bar=False,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    device=self.device
                )
        except Exception:
            embeddings = model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=False,
                normalize_embeddings=True,
                convert_to_numpy=True
            )
            
        if hasattr(embeddings, "cpu"):
            embeddings = embeddings.cpu().numpy()
        elif not isinstance(embeddings, np.ndarray):
            embeddings = np.array(embeddings, dtype=np.float32)
            
        gc.collect()
        return embeddings.astype(np.float32)
