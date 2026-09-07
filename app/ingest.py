import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from pptx import Presentation


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge"
OUTPUT_FILE = BASE_DIR / "data" / "course_chunks.json"


# --------------------------------------------------
# Read different file types
# --------------------------------------------------

def read_text_file(file_path):
    return file_path.read_text(encoding="utf-8")


def read_pdf_file(file_path):
    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def read_pptx_file(file_path):
    presentation = Presentation(str(file_path))

    slides = []

    for slide in presentation.slides:

        slide_text = []

        for shape in slide.shapes:

            if hasattr(shape, "text") and shape.text:
                slide_text.append(shape.text)

        if slide_text:
            slides.append("\n".join(slide_text))

    return "\n\n".join(slides)


# --------------------------------------------------
# Determine source type
# --------------------------------------------------

def get_source_type(file_path):

    folder_name = file_path.parent.name

    if folder_name == "course_material":
        return "course_material"

    if folder_name == "class_topics":
        return "class_topic"

    if folder_name == "readings":
        return "reading"

    if folder_name == "panasonic":
        return "primary_research"

    if folder_name == "group_research":
        return "student_note"

    return "unknown"


# --------------------------------------------------
# Read a source file
# --------------------------------------------------

def read_source(file_path):

    extension = file_path.suffix.lower()

    if extension == ".txt":
        return read_text_file(file_path)

    if extension == ".pdf":
        return read_pdf_file(file_path)

    if extension == ".pptx":
        return read_pptx_file(file_path)

    return ""


# --------------------------------------------------
# Find knowledge-base files
# --------------------------------------------------

source_files = []

for file_path in KNOWLEDGE_DIR.rglob("*"):

    if not file_path.is_file():
        continue

    if file_path.name == ".gitkeep":
        continue

    if file_path.suffix.lower() in [".txt", ".pdf", ".pptx"]:
     if file_path.name == "course_handout.pdf":
        continue

     source_files.append(file_path)

print(f"Found {len(source_files)} source files.")


# --------------------------------------------------
# Chunking
# --------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


# --------------------------------------------------
# Create documents
# --------------------------------------------------

documents = []

next_id = 0

for source_file in source_files:

    print(f"Reading: {source_file.name}")

    text = read_source(source_file)

    if not text.strip():
        print(f"Warning: No text extracted from {source_file.name}")
        continue

    chunks = splitter.split_text(text)

    source_type = get_source_type(source_file)

    for chunk in chunks:

        documents.append({
            "id": next_id,
            "text": chunk,
            "source": source_file.name,
            "source_type": source_type
        })

        next_id += 1


# --------------------------------------------------
# Save chunks
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE.write_text(
    json.dumps(
        documents,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)


print(f"\nCreated {len(documents)} chunks.")
print(f"Saved to: {OUTPUT_FILE}")