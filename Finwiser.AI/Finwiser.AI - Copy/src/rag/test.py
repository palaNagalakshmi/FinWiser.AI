import sys
import os
sys.path.append(os.path.abspath("../.."))

from src.preprocessing.chunking import generate_chunks
from src.rag.embeddings import EmbeddingModel
from src.rag.vector_store import PineconeVectorStore

chunks = generate_chunks()

embedder = EmbeddingModel()
embeddings = embedder.embed_texts([c["text"] for c in chunks])

store = PineconeVectorStore()
store.upsert_chunks(chunks, embeddings)

print("✅ Vectors uploaded to Pinecone")
