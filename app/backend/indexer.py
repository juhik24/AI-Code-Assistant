from pathlib import Path

from app.backend.file_loader import load_files
from app.backend.chunker import chunk_documents
from app.backend.embedder import generate_embeddings
from app.backend.vector_store import reset_collection, store_chunks

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def index_repository(project_path, session_id):
    documents = load_files(project_path)

    chunks = chunk_documents(documents)

    chunks = generate_embeddings(chunks)

    reset_collection(session_id)
    store_chunks(chunks, session_id)

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "message": "Repository indexed successfully"
    }


if __name__ == "__main__":
    project_path = BASE_DIR / "sample_project"

    result = index_repository(project_path)

    print(result["message"])
    print(f"Loaded {result['documents']} documents")
    print(f"Created {result['chunks']} chunks")