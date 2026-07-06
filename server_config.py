from pathlib import Path

DOCS_DIR = Path("./rag_docs")
DOCS_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".txt", ".md", ".cpp", ".h", ".py", ".json"}

DEFAULT_OLLAMA_MODEL = "gemma4:e2b"
OLLAMA_HOST = "http://127.0.0.1:11434"