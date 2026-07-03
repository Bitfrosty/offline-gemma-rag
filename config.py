from pathlib import Path

DOCS_DIR = Path("./rag_docs")
DOCS_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
".txt",
".md",
".cpp",
".h",
".py",
".json",
".html",
".docx",
".xml",
".js"
}
