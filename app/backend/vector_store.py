import chromadb

client = chromadb.PersistentClient(path="./chroma_db")


def get_collection(session_id):
    return client.get_or_create_collection(
        name=f"session_{session_id}"
    )


def reset_collection(session_id):
    try:
        client.delete_collection(f"session_{session_id}")
    except Exception:
        pass


def store_chunks(chunks, session_id):
    collection = get_collection(session_id)

    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        metadatas=[
            {"source": chunk["source"]}
            for chunk in chunks
        ],
    )

    print(f"Stored {len(chunks)} chunks.")