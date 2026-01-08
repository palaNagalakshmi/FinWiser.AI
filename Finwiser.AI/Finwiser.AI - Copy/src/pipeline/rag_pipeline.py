from src.rag.retriever import Retriever
from src.agents.qa_agent import QAAgent
from src.preprocessing.chunking import generate_chunks


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.qa_agent = QAAgent()

        # Load chunks once (local text store)
        self.chunks = generate_chunks()
        self.chunk_text_lookup = {
            chunk["chunk_id"]: chunk["text"] for chunk in self.chunks
        }

    def ask(self, question: str):
        retrieved_chunks = self.retriever.retrieve(question)

        return self.qa_agent.answer(
            question=question,
            chunks=retrieved_chunks,
            chunk_text_lookup=self.chunk_text_lookup
        )
