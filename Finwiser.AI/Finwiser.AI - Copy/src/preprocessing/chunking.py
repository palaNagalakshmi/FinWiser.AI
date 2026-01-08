import os
from typing import List, Dict

# Directory where SEC filing text files are stored
INPUT_DIR = "data/filings_text"

# Chunking parameters
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def clean_text(text: str) -> str:
    """
    Normalize SEC filing text to be Pinecone-safe.
    - Replaces smart quotes
    - Removes corrupted / non-UTF8 characters
    """

    # Normalize smart quotes
    text = (
        text.replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2018", "'")
            .replace("\u2019", "'")
    )

    # Remove any remaining invalid / corrupted characters
    text = text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

    return text


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Split text into overlapping word-based chunks.
    """
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start = end - overlap

    return chunks


def parse_filename(filename: str) -> Dict[str, str]:
    """
    Extract metadata from filename.
    Expected format: TICKER_FORMTYPE_YEAR.txt
    Example: BKH_10-K_2009-03-02.txt
    """
    name = filename.replace(".txt", "")
    parts = name.split("_")

    return {
        "ticker": parts[0],
        "form_type": parts[1] if len(parts) > 1 else "unknown",
        "filed_year": parts[2] if len(parts) > 2 else "unknown",
        "source_file": filename
    }


def generate_chunks() -> List[Dict]:
    """
    Read SEC filing text files, clean them, chunk them,
    and attach metadata + chunk IDs.
    """
    all_chunks = []

    for file in os.listdir(INPUT_DIR):
        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(INPUT_DIR, file)

        with open(file_path, "r", encoding="utf-8") as f:
            text = clean_text(f.read())

        metadata = parse_filename(file)
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for idx, chunk in enumerate(chunks):
            chunk_id = f"{metadata['ticker']}_{metadata['form_type']}_{metadata['filed_year']}_{idx}"

            all_chunks.append({
                "chunk_id": chunk_id,
                "text": chunk,
                "metadata": metadata
            })

    print(f"Generated {len(all_chunks)} chunks")
    return all_chunks


if __name__ == "__main__":
    chunks = generate_chunks()
    print(chunks[0])
