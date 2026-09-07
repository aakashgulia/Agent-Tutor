import json
from pathlib import Path

from embeddings import create_embedding


BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_FILE = BASE_DIR / "data" / "course_chunks.json"
INDEX_FILE = BASE_DIR / "data" / "course_index.json"


# Load course chunks
chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))

index = []

for i, chunk in enumerate(chunks):
    print(f"Embedding chunk {i + 1}/{len(chunks)}...")

    vector = create_embedding(chunk["text"])

    index.append({
        "id": chunk["id"],
        "text": chunk["text"],
        "source": chunk["source"],
        "source_type": chunk["source_type"],
        "embedding": vector
    })


# Save the index
INDEX_FILE.write_text(
    json.dumps(index, ensure_ascii=False),
    encoding="utf-8"
)

print(f"\nCreated index with {len(index)} chunks.")
print(f"Saved to: {INDEX_FILE}")