from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from pathlib import Path
import shutil
import requests

from rag import retrieve_context
from ingest import ingest_file
from debug_logger import get_logger
from config import DOCS_DIR, ALLOWED_EXTENSIONS

logger = get_logger(__name__)

LLAMA_SERVER_URL = "http://127.0.0.1:11434/v1/chat/completions"

from config import DOCS_DIR, ALLOWED_EXTENSIONS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    user_id: str
    chat_id: str
    message: str
    messages: list[ChatMessage] = []


class DebugRequest(BaseModel):
    message: str
    data: dict = {}


def call_gemma(
    user_message: str,
    context_chunks: list[str],
    messages: list[ChatMessage]
) -> str:
    logger.info("Calling llama-server")
    logger.debug(f"User message: {user_message}")
    logger.debug(f"Context chunks found: {len(context_chunks)}")
    logger.debug(f"Conversation messages received: {len(messages)}")

    context_text = "\n\n---\n\n".join(context_chunks)
    logger.debug(context_text)

    final_user_prompt = f"""
Use this retrieved context only if it is relevant.

Retrieved context:
{context_text}

User question:
{user_message}
"""

    conversation = []
    last_role = None
    seen_user_message = False

    for msg in messages[-10:]:
        role = msg.role
        content = msg.content.strip()

        if role not in ["user", "assistant"]:
            continue

        if not content:
            continue

        # Ignore frontend/status messages
        if "File embedded successfully" in content:
            continue

        if "Chunks Added:" in content:
            continue

        if "Error connecting to llama-server" in content:
            continue

        # Skip duplicate current user message because we add the RAG prompt below
        if role == "user" and content == user_message:
            continue

        # Do not allow history to start with assistant
        if not seen_user_message and role == "assistant":
            continue

        if role == "user":
            seen_user_message = True

        # Enforce user/assistant alternation
        if role == last_role:
            continue

        conversation.append({
            "role": role,
            "content": content
        })

        last_role = role

    # Make sure the final history message is not user before adding final prompt
    if conversation and conversation[-1]["role"] == "user":
        conversation.pop()

    conversation.append({
        "role": "user",
        "content": final_user_prompt
    })
    payload = {
        "model": "gemma4:e2b",
        "messages": conversation,
        "temperature": 0.7,
        "stream": False
    }

    logger.debug(f"Payload sent to llama-server: {payload}")

    response = requests.post(
        LLAMA_SERVER_URL,
        json=payload,
        timeout=120
    )

    if not response.ok:
        logger.error("LLAMA SERVER ERROR")
        logger.error(f"Status code: {response.status_code}")
        logger.error(f"Response text: {response.text}")
        logger.error(f"Payload sent: {payload}")

    response.raise_for_status()

    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    logger.info("Received response from llama-server")
    logger.debug(f"Answer: {answer}")

    return answer


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    chat_id: str = Form(...)
):
    logger.info(f"Upload request received: {file.filename}")

    try:
        suffix = Path(file.filename).suffix.lower()

        if suffix not in ALLOWED_EXTENSIONS:
            return {
                "success": False,
                "error": f"Unsupported file type: {suffix}"
            }

        safe_name = Path(file.filename).name

        user_docs_dir = DOCS_DIR / user_id
        user_docs_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_docs_dir / safe_name

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunks_added = ingest_file(
            file_path,
            user_id,
            chat_id
        )

        return {
            "success": True,
            "filename": safe_name,
            "chunks_added": chunks_added,
            "message": f"Uploaded and embedded {safe_name}"
        }

    except Exception as error:
        logger.exception(f"Upload failed for {file.filename}")

        return {
            "success": False,
            "error": str(error)
        }


@app.post("/chat")
def chat(request: ChatRequest):
    logger.info("Chat request received")

    try:
        context_chunks = retrieve_context(
            request.message,
            request.user_id,
            request.chat_id,
            top_k=5
        )

        answer = call_gemma(
            request.message,
            context_chunks,
            request.messages
        )

        return {
            "answer": answer,
            "sources_used": context_chunks
        }

    except requests.exceptions.RequestException as error:
        return {
            "answer": f"Error connecting to llama-server: {str(error)}"
        }

    except Exception as error:
        return {
            "answer": f"Backend error: {str(error)}"
        }

@app.post("/debug")
def debug_from_frontend(request: DebugRequest):
    logger.debug(f"Frontend debug: {request.message} | Data: {request.data}")

    return {
        "success": True,
        "message": "Debug message logged"
    }


app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)
