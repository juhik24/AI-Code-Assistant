import shutil
import uuid
import zipfile
from pathlib import Path
import os
import shutil
import traceback
from fastapi.responses import PlainTextResponse
from fastapi import BackgroundTasks

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.backend.chat import ask
from app.backend.indexer import index_repository
from app.backend.progress import progress
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
    allow_origins=[
        "http://localhost:5173",
        "https://ai-code-assistant-sage.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GitHubRequest(BaseModel):
    repo_url: str

class ChatRequest(BaseModel):
    session_id: str
    question: str

def background_index(project_path, session_id):
    try:
        index_repository(project_path, session_id)
    finally:
        shutil.rmtree(project_path.parent, ignore_errors=True)


@app.post("/index")
def index():
    result = index_repository()
    return result

# @app.post("/chat")
# def chat(request: ChatRequest):
#     return ask(
#         request.question,
#         request.session_id
#     )


@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        return ask(req.session_id, req.question)
    except Exception:
        return PlainTextResponse(
            traceback.format_exc(),
            status_code=500,
        )

@app.get("/history/{session_id}")
def history(session_id: str):
    return {
        "messages": get_history(session_id)
    }

@app.post("/upload")
async def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
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

    create_session(
        session_id=session_id,
        repository_name=file.filename
    )

    background_tasks.add_task(
        background_index,
        project_path,
        session_id
    )

    return {
        "session_id": session_id,
        "message": "Indexing started"
    }

@app.post("/github")
async def index_github(request: GitHubRequest, background_tasks: BackgroundTasks,):
    session_id = str(uuid.uuid4())

    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir()

    project_path = session_dir / "repo"

    clone_repository(request.repo_url, project_path)

    create_session(
        session_id=session_id,
        repository_name=request.repo_url
    )

    background_tasks.add_task(
        background_index,
        project_path,
        session_id
    )

    return {
        "session_id": session_id,
        "message": "Indexing started"
    }

@app.get("/progress/{session_id}")
async def get_progress(session_id: str):
    print("Requested:", session_id)
    print("Available:", list(progress.keys()))

    if session_id not in progress:
        return {
            "status": "starting",
            "stage": "Initializing",
            "completed": 0,
            "total": 0,
            "percentage": 0,
        }

    return progress[session_id]


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-health")
def db_health():
    from app.database.mongo import chat_history
    return {
        "count": chat_history.count_documents({})
    }