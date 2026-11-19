from pathlib import Path
import chromadb
from pypdf import PdfReader
from app.config import client

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PDF_DIR = PROJECT_ROOT / "data" / "job_descriptions"
COLLECTION_NAME = "job_descriptions"
EMBEDDING_MODEL = "text-embedding-3-small"


def position_from_file(pdf_path):
    """'Python Dev Job Description.pdf' -> 'Python Dev'"""
    return pdf_path.stem.replace("Job Description", "").strip()

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def split_text(text, chunk_size=500, overlap=100):
    """Split the text into fixed-size chunks; each chunk overlaps the previous one by `overlap` chars"""
    text = " ".join(text.split())
    chunks = []

    for start in range(0, len(text), chunk_size - overlap):
        chunks.append(text[start:start + chunk_size])
    return chunks

def build_vector_db():
    """Embed the PDFs with the OpenAI API and store them in an in-memory (ephemeral) Chroma"""
    chroma_client = chromadb.Client()

    collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

    for pdf_path in PDF_DIR.glob("*.pdf"):
        position = position_from_file(pdf_path)
        chunks = split_text(read_pdf(pdf_path))

        response = client.embeddings.create(input=chunks, model=EMBEDDING_MODEL)
        embeddings = [d.embedding for d in response.data]

        collection.upsert(
            ids= [f"{pdf_path.stem}_{i}" for i in range(len(chunks))],
            documents=chunks,
            embeddings = embeddings,
            metadatas=[{"source": pdf_path.name, "position": position, "chunk": i} for i in range(len(chunks))],
        )
        print(f"{position}: {len(chunks)} chunks embedded")

    return collection
