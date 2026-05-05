from flask import Blueprint, request, jsonify
from services.llm_client import call_llm
from services.rag_pipeline import search_docs
from datetime import datetime
import json

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'query' field"}), 400

    # Step 1: Retrieve context
    results = search_docs(query, n_results=3)
    context_chunks = results["documents"][0]

    # Step 2: Build prompt with context
    prompt = f"""
    User query: "{query}"
    Relevant context:
    {context_chunks}

    Generate 3 actionable recommendations.
    Each must include:
    - action_type
    - description
    - priority
    Return as a valid JSON array only.
    """

    raw_output = call_llm(prompt)

    # Step 3: Clean + parse JSON
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
    cleaned = cleaned.replace("json", "").strip()

    try:
        recommendations = json.loads(cleaned)
    except Exception:
        recommendations = []

    return jsonify({
        "query": query,
        "recommendations": recommendations,
        "context_used": context_chunks,
        "generated_at": datetime.utcnow().isoformat()
    })
