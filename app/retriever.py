import json
import math
import re
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "data" / "course_index.json"


def tokenize(text):
    """Convert text into lowercase searchable terms."""
    return re.findall(r"\b[a-zA-Z0-9]+\b", str(text).lower())


def retrieve_chunks(question, top_k=3):
    """
    Retrieve course chunks using BM25 keyword ranking.

    Uses only Python's standard library. No Ollama, embeddings,
    or external AI API is required for retrieval.
    """
    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Course index was not found: {INDEX_FILE}"
        )

    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))

    if not isinstance(index, list) or not index:
        return []

    query_terms = tokenize(question)

    if not query_terms:
        return []

    documents = [
        tokenize(item.get("text", ""))
        for item in index
    ]

    document_count = len(documents)
    document_lengths = [len(document) for document in documents]
    average_length = (
        sum(document_lengths) / document_count
        if document_count else 0
    )

    if average_length == 0:
        return []

    document_frequency = Counter()
    for document in documents:
        document_frequency.update(set(document))

    k1 = 1.5
    b = 0.75

    results = []

    for item, terms, document_length in zip(
        index, documents, document_lengths
    ):
        term_counts = Counter(terms)
        score = 0.0

        for term in query_terms:
            frequency = term_counts.get(term, 0)

            if frequency == 0:
                continue

            df = document_frequency.get(term, 0)
            idf = math.log(
                1 + (document_count - df + 0.5) / (df + 0.5)
            )

            denominator = frequency + k1 * (
                1 - b + b * document_length / average_length
            )

            score += idf * (
                frequency * (k1 + 1) / denominator
            )

        results.append({
            "id": item.get("id"),
            "text": item.get("text", ""),
            "source": item.get("source", "Unknown source"),
            "source_type": item.get("source_type", "Unknown"),
            "score": score
        })

    results.sort(key=lambda result: result["score"], reverse=True)

    matched_results = [
        result for result in results
        if result["score"] > 0
    ]

    return matched_results[:top_k]
