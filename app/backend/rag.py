from app.backend.vector_store import get_collection
from app.backend.embedder import get_embedding


def retrieve_context(question, session_id, top_k=10):

    collection = get_collection(session_id)

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )

    return results