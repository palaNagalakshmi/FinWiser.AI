from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.rag_pipeline import RAGPipeline

app = FastAPI(
    title="FINWISER.AI – SEC Filing Q&A",
    description="Ask questions over SEC 10-K / 10-Q filings with grounded answers and citations",
    version="1.0"
)

pipeline = RAGPipeline()


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """
    Ask an investor-focused question over indexed SEC filings.
    """
    result = pipeline.ask(request.question)
    return result
