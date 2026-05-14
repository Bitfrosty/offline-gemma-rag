import os
import requests
import numpy as np
from pymongo import MongoClient

from debug_logger import get_logger

logger = get_logger(__name__)

OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"
EMBED_MODEL = "nomic-embed-text"

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

logger.info(f"Connecting to MongoDB at: {MONGO_URI}")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["rag_database"]
collection = db["rag_memory"]


def embed_text(text: str) -> list[float]:
    logger.debug(f"Requesting embedding. Text length: {len(text)}")

    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "input": text
        },
        timeout=60
    )

    if not response.ok:
        logger.error("Embedding request failed")
        logger.error(f"Status code: {response.status_code}")
        logger.error(f"Response text: {response.text}")

    response.raise_for_status()

    data = response.json()
    embedding = data["embeddings"][0]

    logger.debug(f"Received embedding with length: {len(embedding)}")

    return embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a)
    b = np.array(b)

    return float(
        np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    )


def retrieve_context(query: str, chat_id: str, top_k: int = 5) -> list[str]:
    logger.info(f"Retrieving context for query: {query}")

    query_embedding = embed_text(query)

    docs = list(collection.find(
        {"chat_id": chat_id},
        {
            "_id": 0,
            "text": 1,
            "embedding": 1,
            "source": 1,
            "chunk_index": 1,
            "chat_id": 1
        }
    ))

    logger.debug(f"Documents loaded from MongoDB: {len(docs)}")

    scored_docs = []

    for doc in docs:
        score = cosine_similarity(
            query_embedding,
            doc["embedding"]
        )

        scored_docs.append({
            "text": doc["text"],
            "score": score,
            "source": doc.get("source"),
            "chunk_index": doc.get("chunk_index")
        })

    scored_docs.sort(
        key=lambda doc: doc["score"],
        reverse=True
    )

    relevant_docs = [
        doc for doc in scored_docs[:top_k]
        if doc["score"] >= 0.50
    ]

    logger.info(f"Relevant chunks found: {len(relevant_docs)}")

    for doc in relevant_docs:
        logger.debug(
            f"Score={doc['score']} Source={doc['source']} Chunk={doc['chunk_index']}"
        )

    return [doc["text"] for doc in relevant_docs]