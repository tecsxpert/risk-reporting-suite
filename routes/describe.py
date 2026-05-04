from flask import Blueprint, request, jsonify
from services.chroma_client import collection, model

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/", methods=["POST"])
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
