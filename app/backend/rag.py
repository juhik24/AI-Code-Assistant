from app.backend.vector_store import get_collection
from app.backend.embedder import model


def retrieve_context(question, session_id, top_k=10):
    collection = get_collection(session_id)

    question_embedding = model.encode(
        question,
        convert_to_numpy=True
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )
    print(results["documents"])
    print(results["metadatas"])

    return results