import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="documents")


def retrieve_context(question: str, top_k: int = 3):

    # Convert question to embedding
    query_embedding = embedding_model.encode(question).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    sources = []

    for meta in metadatas:
        if meta and "source" in meta:
            sources.append(meta["source"])

    return context, sources