import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_FILE = BASE_DIR / "data" / "course_chunks.json"
INDEX_FILE = BASE_DIR / "data" / "course_index.json"


def build_index():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Course chunks file was not found: {CHUNKS_FILE}"
        )

    chunks = json.loads(
        CHUNKS_FILE.read_text(encoding="utf-8")
    )

    if not isinstance(chunks, list):
        raise ValueError(
            "course_chunks.json must contain a JSON list."
        )

    index = []

    for number, chunk in enumerate(chunks, start=1):
        required_fields = ("id", "text", "source", "source_type")
        missing_fields = [
            field for field in required_fields
            if field not in chunk
        ]

        if missing_fields:
            raise ValueError(
                f"Chunk {number} is missing required fields: "
                + ", ".join(missing_fields)
            )

        print(f"Preparing chunk {number}/{len(chunks)}...")

        # BM25 uses the original text directly.
        # No embedding model or external AI service is required.
        index.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "source": chunk["source"],
            "source_type": chunk["source_type"]
        })

    # Write to a temporary file first so an existing index is not
    # overwritten if writing the new index fails.
    temporary_file = INDEX_FILE.with_suffix(".json.tmp")

    temporary_file.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    temporary_file.replace(INDEX_FILE)

    print(f"\nCreated BM25 index with {len(index)} chunks.")
    print(f"Saved to: {INDEX_FILE}")


if __name__ == "__main__":
    build_index()
