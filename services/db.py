import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_or_create_collection("risk_docs")
model = SentenceTransformer("all-MiniLM-L6-v2")
