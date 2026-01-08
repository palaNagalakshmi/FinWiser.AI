import os
from typing import List, Dict
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "finwiser-sec-rag"

class PineconeVectorStore:
    def __init__(self, dimension: int = 384):
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY environment variable not set")

        pc = Pinecone(api_key=PINECONE_API_KEY)

        existing_indexes = [idx["name"] for idx in pc.list_indexes()]

        if INDEX_NAME not in existing_indexes:
            pc.create_index(
                name=INDEX_NAME,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        self.index = pc.Index(INDEX_NAME)

    def upsert_chunks(self, chunks: List[Dict], embeddings: List[List[float]]):
        """
        Store ONLY embeddings + lightweight metadata in Pinecone.
        DO NOT store raw text in metadata.
        """
        vectors = []

        for chunk, embedding in zip(chunks, embeddings):
            vectors.append({
                "id": chunk["chunk_id"],
                "values": embedding,
                "metadata": {
                    "ticker": chunk["metadata"]["ticker"],
                    "form_type": chunk["metadata"]["form_type"],
                    "filed_year": chunk["metadata"]["filed_year"],
                    "source_file": chunk["metadata"]["source_file"]
                }
            })
        self.index.upsert(vectors=vectors)

    def query(self, query_embedding: List[float], top_k: int = 5):
        return self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
