import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.backend.rag import retrieve_context
from app.services.chat_history_service import append_message

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

#print(os.getenv("GEMINI_API_KEY"))  # Temporary

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def build_prompt(question: str, contexts: list[str]) -> str:
    context = "\n\n".join(contexts)

    return f"""
You are an AI assistant that answers questions about a codebase.

Use ONLY the provided context.

If the answer is not present in the context, say:
"I couldn't find that in the indexed code."

Context:
{context}

Question:
{question}
"""


def ask(question, session_id):
    # Save user question
    append_message(
        session_id=session_id,
        role="user",
        content=question,
    )

    results = retrieve_context(question, session_id)

    contexts = results["documents"][0]
    metadatas = results["metadatas"][0]

    prompt = build_prompt(question, contexts)

    print("========== CONTEXT ==========")
    print(contexts)
    print("=============================")

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )

    sources = list(
        dict.fromkeys(
            metadata["source"] for metadata in metadatas
        )
    )

    # Save assistant response
    append_message(
        session_id=session_id,
        role="assistant",
        content=response.text,
        sources=sources,
    )

    return {
        "answer": response.text,
        "sources": sources,
    }