import json
import math
from pathlib import Path

from embeddings import create_embedding


BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "data" / "course_index.json"


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_chunks(question, top_k=3):
    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))

    question_embedding = create_embedding(question)

    results = []

    for item in index:
        score = cosine_similarity(
            question_embedding,
            item["embedding"]
        )

        results.append({
            "id": item["id"],
            "text": item["text"],
            "source": item["source"],
            "source_type": item["source_type"],
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]
