import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")

# -----------------------------
# Lazy load model (IMPORTANT FIX)
# -----------------------------
embedding_model = None


def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return embedding_model


def retrieve_context(question: str, top_k: int = 3):

    model = get_embedding_model()

    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    context = "\n\n".join(documents) if documents else ""

    sources = []

    for meta in metadatas:
        if meta and "source" in meta:
            sources.append(meta["source"])

    return context, sources