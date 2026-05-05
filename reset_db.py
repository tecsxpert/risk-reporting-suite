import chromadb

# Point to the same persistent path
client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_or_create_collection("risk_docs")

#  Delete all documents by fetching their IDs first
all_docs = collection.get()
if all_docs["ids"]:
    collection.delete(ids=all_docs["ids"])
    print("✅ Collection cleared. All documents removed.")
else:
    print("⚠️ No documents found to delete.")
