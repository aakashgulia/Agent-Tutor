import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = BASE_DIR / "knowledge" / "course_material" / "course_handout.txt"
OUTPUT_FILE = BASE_DIR / "data" / "course_chunks.json"


# Read the course handout
text = SOURCE_FILE.read_text(encoding="utf-8")


# Split the text into manageable chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = splitter.split_text(text)


# Store chunks with basic source information
documents = []

for i, chunk in enumerate(chunks):
    documents.append({
        "id": i,
        "text": chunk,
        "source": "course_handout.pdf",
        "source_type": "course_material"
    })


# Save the chunks
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE.write_text(
    json.dumps(documents, indent=2, ensure_ascii=False),
    encoding="utf-8"
)


print(f"Created {len(documents)} chunks.")
print(f"Saved to: {OUTPUT_FILE}")