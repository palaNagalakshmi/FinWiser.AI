FINWISER.AI — SEC Filing Summarizer & Q&A using RAG
* Problem Statement
Problem:
Enable users to query SEC 10-K / 10-Q filings and receive investor-focused answers that are:

Grounded strictly in filings
Transparent with source citations
Safe from hallucinations
_____________________________________________________________________________________________________________________________________________________________________________
Dataset:
SEC Filings – Kaggle

https://www.kaggle.com/datasets/kharanshuvalangar/sec-filings
_____________________________________________________________________________________________________________________________________________________________________________
Expected Outcome:

Index a curated subset of filings
Implement ask(question)
Return:
✅ Grounded answer
✅ Chunk-level citations
Refuse safely when data is unavailable
_____________________________________________________________________________________________________________________________________________________________________________
Project Vision
FINWISER.AI is a Retrieval-Augmented Generation (RAG) system designed for accuracy, explainability, and trust in financial Q&A.

Instead of letting an LLM guess, FINWISER.AI:

Retrieves relevant SEC filing chunks
Generates answers only from retrieved evidence
Explicitly cites the filing sections used
This project prioritizes correctness over creativity, making it suitable for investor-facing use cases.
_____________________________________________________________________________________________________________________________________________________________________________
Key Features
✅ SEC filing ingestion & parsing
✅ Robust text chunking with overlap
✅ Semantic retrieval using Pinecone
✅ Sentence-Transformer embeddings
✅ FastAPI backend (/ask endpoint)
✅ Citation-backed answers
✅ Safe refusal when information is missing
✅ Streamlit UI for demo & evaluation
____________________________________________________________________________________________________________________________________________________________________________
 Guardrails & Safety Mechanisms (Core Strength)
FINWISER.AI implements explicit guardrails to ensure reliability and prevent hallucinations.

1️⃣ Retrieval-Only Answering
The LLM never answers directly from its own knowledge
All answers are generated only from retrieved SEC filing chunks
If no relevant chunks are retrieved, the system refuses to answer
"Insufficient information found in the selected SEC filings."
_____________________________________________________________________________________________________________________________________________________________________________
2️⃣ Mandatory Source Citations
Every answer is accompanied by chunk-level citations
Citations reference:
Company ticker
Filing type (10-K / 10-Q)
Filing date
Chunk index
This guarantees traceability and auditability of responses.
_____________________________________________________________________________________________________________________________________________________________________________
3️⃣ Safe Refusal Policy
The system explicitly refuses to answer if:

Retrieval confidence is too low
Context does not contain the answer
The question is out-of-scope
➡️ This prevents speculative or hallucinated responses.
_____________________________________________________________________________________________________________________________________________________________________________
4️⃣ Prompt-Level Constraints
The LLM is instructed with a strict system prompt:

Answer only from provided context
Do not infer or speculate
Refuse if the answer is not present
This acts as a second-layer guardrail on top of retrieval.
____________________________________________________________________________________________________________________________________________________________________________-
5️⃣ No External Knowledge Leakage
The Streamlit UI is a thin client
All reasoning happens in the FastAPI backend
Users cannot inject external context or bypass retrieval
_____________________________________________________________________________________________________________________________________________________________________________
6️⃣ Deterministic & Explainable Output
Chunk IDs are preserved end-to-end
Every answer can be manually verified against the original filing
Designed for compliance-focused and audit-friendly use cases
 Why This Project Stands Out
Aspect	Typical Submissions	FINWISER.AI
Dataset usage	Full dump	Curated subset
Answers	Ungrounded LLM	Retrieval-grounded
Citations	Missing	Chunk-level
Backend	Notebook demo	FastAPI service
Safety	Hallucinations	Explicit refusal
UI	Optional	Thin API client
_____________________________________________________________________________________________________________________________________________________________________________
 High-Level Architecture
User Question
↓
Streamlit UI (frontend)
↓
FastAPI Backend (/ask)
↓
Embedding Model
↓
Pinecone Vector Search
↓
Relevant SEC Chunks
↓
LLM Answer Generation
↓
Answer + Citations
_____________________________________________________________________________________________________________________________________________________________________________
🛠️ Tech Stack
Core
Python 3.10+
FastAPI – backend API
Pinecone – vector database
Sentence-Transformers – embeddings
OpenAI API – answer generation
_____________________________________________________________________________________________________________________________________________________________________________
Data & Processing
requests
pandas
unstructured
_____________________________________________________________________________________________________________________________________________________________________________
Frontend
Streamlit (API consumer only)
_____________________________________________________________________________________________________________________________________________________________________________
 Final Folder Structure
FinWiser.AI/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env
├── app.py # Streamlit UI (API client)
├── test_rag.py # Local RAG testing
│
├── data/
│ ├── sec_filings.csv # Kaggle metadata
│ └── filings_text/ # Downloaded filing text (generated)
│
├── src/
│ ├── agents/
│ │ └── qa_agent.py
│ │
│ ├── api/
│ │ └── main.py # FastAPI app (/ask)
│ │
│ ├── ingestion/
│ │ └── fetch_filings.py
│ │
│ ├── preprocessing/
│ │ └── chunking.py
│ │
│ ├── rag/
│ │ ├── embeddings.py
│ │ ├── vector_store.py
│ │ ├── retriever.py
│ │ └── test.py
│ │
│ └── pipeline/
│ └── rag_pipeline.py
│
└── logs/
_____________________________________________________________________________________________________________________________________________________________________________
📥 Data Flow Explained
1️⃣ Input Data
sec_filings.csv
Metadata file from Kaggle containing filing URLs and company details.
2️⃣ Generated Data
filings_text/
SEC filing text downloaded via ingestion script.
 filings_text/ is generated and excluded from version control.
_____________________________________________________________________________________________________________________________________________________________________________
 RAG Workflow
Indexing Phase
Load metadata
Select a small set of companies
Download SEC filings
Chunk text (800 tokens, 100 overlap)
Generate embeddings
Store vectors in Pinecone
Question Phase
User submits question
Embed the question
Retrieve top-k relevant chunks
Generate answer using retrieved context only
Attach citations
____________________________________________________________________________________________________________________________________________________________________________
 Example API Output
{
  "answer": "The plan provides outside directors with stock-based compensation aligned with shareholder interests.",
  "sources": [
    "BKH_10-K_2009-03-02_4",
    "BKH_10-K_2009-03-02_2"
  ]
}
____________________________________________________________________________________________________________________________________________________________________________
 Running the Project
Start Backend

uvicorn src.api.main:app --reload
Start Frontend

streamlit run app.py
_____________________________________________________________________________________________________________________________________________________________________________
🏁 One-Line Summary
FINWISER.AI is a production-style RAG system that enables investors to ask questions over SEC filings and receive accurate, citation-backed answers through a FastAPI backend and Streamlit demo UI.
