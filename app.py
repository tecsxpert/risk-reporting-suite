from flask import Flask, request, jsonify
import chromadb
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# ✅ Persistent storage
client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_or_create_collection("risk_docs")

model = SentenceTransformer("all-MiniLM-L6-v2")

@app.route("/")
def home():
    return "✅ Risk Reporting AI Service is running!"

@app.route("/describe", methods=["POST"])
def describe():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    embedding = model.encode(text).tolist()
    doc_id = f"{text[:10]}_{len(text)}"
    collection.add(documents=[text], embeddings=[embedding], ids=[doc_id])

    return jsonify({
        "message": "Text stored successfully",
        "document": text,
        "embedding_preview": embedding[:5]
    })

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'query' field"}), 400

    embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=3)

    return jsonify({
        "query": query,
        "recommendations": results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask
from routes.describe import describe_bp
from routes.recommend import recommend_bp

app = Flask(__name__)
app.register_blueprint(describe_bp, url_prefix="/describe")
app.register_blueprint(recommend_bp, url_prefix="/recommend")

@app.route("/")
def home():
    return "✅ Risk Reporting AI Service is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)