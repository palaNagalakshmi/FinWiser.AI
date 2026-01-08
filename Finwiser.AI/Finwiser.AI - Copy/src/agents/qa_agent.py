from typing import List, Dict
from openai import OpenAI
import os


class QAAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def answer(
        self,
        question: str,
        chunks: List[Dict],
        chunk_text_lookup: Dict[str, str]
    ) -> Dict:

        if not chunks:
            return {
                "answer": "Insufficient information found in the selected SEC filings.",
                "sources": []
            }

        context_blocks = []
        sources = []

        for chunk in chunks:
            chunk_id = chunk["chunk_id"]
            text = chunk_text_lookup.get(chunk_id)

            if text:
                context_blocks.append(f"[{chunk_id}]\n{text}")
                sources.append(chunk_id)

        context = "\n\n".join(context_blocks)

        prompt = f"""
You are an SEC filings assistant.

Answer the question using ONLY the information below.
If the answer is not present, say:
"Insufficient information found in the selected SEC filings."

Context:
{context}

Question:
{question}
"""

        response = self.client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You answer strictly from SEC filings."},
                {"role": "user", "content": prompt}
            ]
        )

        answer_text = response.choices[0].message.content.strip()

        if "Insufficient information" in answer_text:
            return {
                "answer": answer_text,
                "sources": []
            }

        return {
            "answer": answer_text,
            "sources": list(set(sources))
        }
