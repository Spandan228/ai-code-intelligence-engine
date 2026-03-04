from typing import List, Dict, Any
from indexer.embedding_generator import EmbeddingGenerator
from vector_store.faiss_index import FaissIndex

class SemanticSearch:
    def __init__(self, embedding_gen: EmbeddingGenerator, vector_store: FaissIndex):
        self.embedding_gen = embedding_gen
        self.vector_store = vector_store
        self.vector_store.load()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_gen.generate([query])
        raw_results = self.vector_store.search(query_embedding, top_k)
        
        formatted_results = []
        for metadata, score in raw_results:
            result = metadata.copy()
            result["score"] = score
            formatted_results.append(result)
            
        return formatted_results
