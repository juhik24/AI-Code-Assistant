from pathlib import Path

from app.backend.file_loader import load_files
from app.backend.chunker import chunk_documents
from app.backend.embedder import generate_embeddings
from app.backend.vector_store import reset_collection, store_chunks
from app.backend.progress import progress   # NEW

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def index_repository(project_path, session_id):

    progress[session_id] = {
        "stage": "Loading files",
        "completed": 0,
        "total": 0,
        "percentage": 0,
        "status": "running",
    }

    documents = load_files(project_path)

    progress[session_id]["stage"] = "Creating chunks"

    chunks = chunk_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    progress[session_id]["stage"] = "Generating embeddings"

    # Pass session_id
    chunks = generate_embeddings(chunks, session_id)

    progress[session_id]["stage"] = "Storing vectors"

    reset_collection(session_id)
    store_chunks(chunks, session_id)

    progress[session_id] = {
        "stage": "Completed",
        "completed": len(chunks),
        "total": len(chunks),
        "percentage": 100,
        "status": "completed",
    }

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "message": "Repository indexed successfully"
    }


if __name__ == "__main__":
    project_path = BASE_DIR / "sample_project"

    result = index_repository(project_path, "demo-session")

    print(result["message"])
    print(f"Loaded {result['documents']} documents")
    print(f"Created {result['chunks']} chunks")