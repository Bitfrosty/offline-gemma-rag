import uuid
from pathlib import Path

from rag import collection, embed_text
from debug_logger import get_logger

logger = get_logger(__name__)

DOCS_DIR = Path("./rag_docs")
ALLOWED_EXTENSIONS = [".txt", ".md", ".cpp", ".h", ".py", ".json"]


def read_file(path: Path) -> str:
    logger.debug(f"Reading file: {path}")

    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    logger.debug(
        f"Chunking text. Length={len(text)}, chunk_size={chunk_size}, overlap={overlap}"
    )

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    logger.debug(f"Created {len(chunks)} chunks")
    return chunks


def ingest_file(path: Path, chat_id: str):
    logger.info(f"Starting ingestion for: {path}")

    if not path.exists():
        logger.error(f"File does not exist: {path}")
        raise FileNotFoundError(f"{path} does not exist")

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        logger.error(f"Unsupported file type: {path.suffix}")
        raise ValueError(f"Unsupported file type: {path.suffix}")

    text = read_file(path)
    chunks = chunk_text(text)

    documents = []

    for index, chunk in enumerate(chunks):
        logger.debug(f"Embedding chunk {index} from {path.name}")

        embedding = embed_text(chunk)

        documents.append({
            "chunk_id": str(uuid.uuid4()),
            "chat_id": chat_id,
            "text": chunk,
            "embedding": embedding,
            "source": str(path),
            "filename": path.name,
            "chunk_index": index
        })

    if documents:
        collection.insert_many(documents)
        logger.info(f"Inserted {len(documents)} chunks from {path.name}")
    else:
        logger.warning(f"No chunks created for {path.name}")

    return len(documents)


def ingest_documents():
    logger.info("Starting full document ingestion")

    files = [
        path for path in DOCS_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS
    ]

    if not files:
        logger.warning("No documents found in rag_docs/")
        return

    for path in files:
        chunks_added = ingest_file(path, "global")
        logger.info(f"Added {chunks_added} chunks from {path.name}")

    logger.info("Ingestion complete")


if __name__ == "__main__":
    ingest_documents()