import json
from flask import Blueprint, request, jsonify
from services.llm_client import call_llm
from datetime import datetime

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'query' field"}), 400

    # Build prompt
    prompt = f"""
    Based on the query: "{query}", generate 3 actionable recommendations.
    Each recommendation must include:
    - action_type (short label like 'monitor', 'hedge', 'alert')
    - description (1–2 sentence explanation)
    - priority (high, medium, low)
    Return them as a valid JSON array only.
    """

    # Call Groq
    raw_output = call_llm(prompt)

    # Step 1a: Clean fenced output
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]  # remove ```json
    cleaned = cleaned.replace("json", "").strip()

    # Step 1b: Parse JSON safely
    try:
        recommendations = json.loads(cleaned)
    except Exception:
        recommendations = []

    # Step 1c: Return structured JSON
    return jsonify({
        "query": query,
        "recommendations": recommendations,
        "generated_at": datetime.utcnow().isoformat()
    })
