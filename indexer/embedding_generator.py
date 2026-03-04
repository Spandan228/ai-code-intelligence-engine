from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.config import EMBEDDING_MODEL_NAME

class EmbeddingGenerator:
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def generate(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.array([])
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return np.array(embeddings)
