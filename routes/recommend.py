from flask import Blueprint, request, jsonify
from services.chroma_client import collection, model

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/", methods=["POST"])
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
