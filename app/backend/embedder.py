import os
import time
import requests
from dotenv import load_dotenv
from app.backend.progress import progress

load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")

API_URL = "https://api.jina.ai/v1/embeddings"

HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
}


def call_embedding_api(payload, session_id=None):
    while True:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
        )

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")

            try:
                wait = int(retry_after)
            except (TypeError, ValueError):
                wait = 60

            if session_id and session_id in progress:
                progress[session_id]["status"] = "waiting"
                progress[session_id]["retry_after"] = wait

            print(f"Rate limit reached. Waiting {wait} seconds...")

            time.sleep(wait)

            if session_id and session_id in progress:
                progress[session_id]["status"] = "running"
                progress[session_id]["retry_after"] = 0

            continue

        print("Status:", response.status_code)
        print("Body:", response.text)
        response.raise_for_status()


def get_embedding(text):
    payload = {
        "model": "jina-embeddings-v3",
        "task": "retrieval.query",
        "input": [text],
    }

    result = call_embedding_api(payload)

    return result["data"][0]["embedding"]


def generate_embeddings(chunks, session_id, batch_size=128):
    total = len(chunks)

    for start in range(0, total, batch_size):

        batch = chunks[start:start + batch_size]
        texts = [chunk["text"] for chunk in batch]

        payload = {
            "model": "jina-embeddings-v3",
            "task": "retrieval.passage",
            "input": texts,
        }

        result = call_embedding_api(payload, session_id)

        embeddings = result["data"]

        for chunk, embedding in zip(batch, embeddings):
            chunk["embedding"] = embedding["embedding"]

        completed = min(start + batch_size, total)

        print("session_id:", session_id)
        print("before:", progress.get(session_id))

        progress[session_id] = {
            "stage": "Generating embeddings",
            "completed": completed,
            "total": total,
            "percentage": int((completed / total) * 100),
            "status": "running",
            "retry_after": 0,
        }

        print("after:", progress.get(session_id))

        progress[session_id] = {
            "stage": "Generating embeddings",
            "completed": completed,
            "total": total,
            "percentage": int((completed / total) * 100),
            "status": "running",
            "retry_after": 0,
        }

        print(
            f"Embedded {completed}/{total} chunks "
            f"({progress[session_id]['percentage']}%)"
        )

    return chunks