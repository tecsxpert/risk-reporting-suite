import chromadb

client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_or_create_collection("risk_docs")

docs = collection.get()
print("Stored documents:", docs["documents"])
