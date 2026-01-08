from typing import List, Dict
from src.rag.embeddings import EmbeddingModel
from src.rag.vector_store import PineconeVectorStore


class Retriever:
    def __init__(self, top_k: int = 5):
        self.embedder = EmbeddingModel()
        self.vector_store = PineconeVectorStore()
        self.top_k = top_k

    def retrieve(self, question: str) -> List[Dict]:
        query_embedding = self.embedder.embed_texts([question])[0]

        results = self.vector_store.query(
            query_embedding=query_embedding,
            top_k=self.top_k
        )

        matches = results.get("matches", [])

        retrieved = []
        for match in matches:
            retrieved.append({
                "chunk_id": match["id"],
                "score": match["score"],
                "metadata": match["metadata"]
            })

        return retrieved
