import shutil
import uuid
import zipfile
from pathlib import Path
import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.backend.chat import ask
from app.backend.indexer import index_repository
from app.backend.github import clone_repository
from app.services.chat_history_service import (
    create_session,
    get_history,
)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GitHubRequest(BaseModel):
    repo_url: str

class ChatRequest(BaseModel):
    session_id: str
    question: str


@app.post("/index")
def index():
    result = index_repository()
    return result

@app.post("/chat")
def chat(request: ChatRequest):
    return ask(
        request.question,
        request.session_id
    )

@app.get("/history/{session_id}")
def history(session_id: str):
    return {
        "messages": get_history(session_id)
    }

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())

    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir()

    zip_path = session_dir / file.filename

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(session_dir)
    
    folders = [
        item
        for item in session_dir.iterdir()
        if item.is_dir()
        and item.name != "__MACOSX"
        and not item.name.startswith(".")
    ]
    if not folders:
        return {
            "message": "No project found inside ZIP."
        }

    project_path = folders[0]
    print(f"Project path: {project_path}")

    try:
        result = index_repository(project_path, session_id)
        create_session(
            session_id=session_id,
            repository_name=file.filename
        )
    finally:
        shutil.rmtree(session_dir, ignore_errors=True)

    return {
        "session_id": session_id,
        **result
    }

@app.post("/github")
async def index_github(request: GitHubRequest):
    session_id = str(uuid.uuid4())

    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir()

    project_path = session_dir / "repo"

    try:
        clone_repository(request.repo_url, project_path)

        result = index_repository(project_path, session_id)
        create_session(
            session_id=session_id,
            repository_name=request.repo_url
        )

    finally:
        shutil.rmtree(session_dir, ignore_errors=True)

    return {
        "session_id": session_id,
        **result,
    }