from datetime import datetime
from app.database.mongo import chat_history


def create_session(session_id, repository_name=None):
    existing = chat_history.find_one({"session_id": session_id})

    if existing:
        return

    chat_history.insert_one({
        "session_id": session_id,
        "repository_name": repository_name,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "messages": []
    })


def append_message(session_id, role, content, sources=None):
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    }

    if sources:
        message["sources"] = sources

    chat_history.update_one(
        {"session_id": session_id},
        {
            "$push": {
                "messages": message
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )


def get_history(session_id):
    conversation = chat_history.find_one(
        {"session_id": session_id},
        {"_id": 0}
    )

    if conversation:
        return conversation.get("messages", [])

    return []


def delete_history(session_id):
    chat_history.delete_one({
        "session_id": session_id
    })