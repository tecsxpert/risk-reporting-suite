from pathlib import Path
from typing import Iterable

import chromadb
from sentence_transformers import SentenceTransformer

ROOT_DIR = Path(__file__).resolve().parents[1]
CHROMA_STORE_DIR = ROOT_DIR / "chroma_store"
COLLECTION_NAME = "risk_docs"

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_chroma_client() -> chromadb.PersistentClient:
    CHROMA_STORE_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_STORE_DIR))


def get_collection(collection_name: str = COLLECTION_NAME):
    client = get_chroma_client()
    return client.get_or_create_collection(collection_name)


# Global collection
collection = get_collection()


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks by character length."""
    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - chunk_overlap)
    return chunks


def load_and_store_docs(docs: Iterable[str], collection_name: str = COLLECTION_NAME) -> str:
    """Load documents, chunk them, embed them, and store them in ChromaDB."""
    docs = [doc for doc in docs if doc and doc.strip()]
    if not docs:
        return "No documents to store."

    collection = get_collection(collection_name)
    total_chunks = 0

    for doc_idx, doc in enumerate(docs):
        chunks = chunk_text(doc, chunk_size=500, chunk_overlap=50)
        for chunk_idx, chunk in enumerate(chunks):
            embedding = model.encode(chunk).tolist()
            record_id = f"doc{doc_idx}_chunk{chunk_idx}"
            payload = {
                "documents": [chunk],
                "embeddings": [embedding],
                "metadatas": [{"doc_idx": doc_idx, "chunk_idx": chunk_idx}],
                "ids": [record_id],
            }

            if hasattr(collection, "upsert"):
                collection.upsert(**payload)
            else:
                collection.add(**payload)

            total_chunks += 1

    return f"Stored {len(docs)} documents with {total_chunks} chunk(s) and embeddings."


def query_similar_documents(query: str, n_results: int = 5, collection_name: str = COLLECTION_NAME) -> list[dict]:
    """Retrieve the most similar stored chunks for a query."""
    if not query or not query.strip():
        return []

    collection = get_collection(collection_name)
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    returned: list[dict] = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, metadata, distance in zip(documents, metadatas, distances):
        returned.append(
            {
                "document": doc,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return returned


def search_docs(query: str, n_results: int = 3):
    embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    return results
