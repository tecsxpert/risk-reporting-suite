import chromadb
from chromadb.config import Settings

class ChromaClient:
    def __init__(self):
        self.client = chromadb.Client(
            Settings(persist_directory="./chroma_db")
        )

        self.collection = self.client.get_or_create_collection(
            name="risk_collection"
        )

    def add_text(self, id, text):
        self.collection.add(
            documents=[text],
            ids=[id]
        )

    def query(self, text):
        results = self.collection.query(
            query_texts=[text],
            n_results=1
        )
        return results