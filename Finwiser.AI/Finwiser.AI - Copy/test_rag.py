from src.pipeline.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

response = pipeline.ask(
    "What does the Outside Directors Stock Based Compensation Plan provide?"
)

print(response)
