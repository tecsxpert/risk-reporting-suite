from flask import Blueprint, request, jsonify
from services.llm_client import call_llm
import json
from datetime import datetime

generate_report_bp = Blueprint("generate_report", __name__)

@generate_report_bp.route("/", methods=["POST"])
def generate_report():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'query' field"}), 400

    # Build prompt for Groq
    prompt = f"""
    Generate a structured report for the topic: "{query}".
    The report must be valid JSON with the following fields:
    - title (short headline)
    - executive_summary (2–3 sentences)
    - overview (detailed explanation, 1–2 paragraphs)
    - top_items (list of 3–5 key points)
    - recommendations (list of 3 actionable recommendations)

    Return only JSON, no extra text.
    """

    raw_output = call_llm(prompt)

    # Clean output
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
    cleaned = cleaned.replace("json", "").strip()

    try:
        report = json.loads(cleaned)
    except Exception:
        report = {
            "title": "Report generation failed",
            "executive_summary": "",
            "overview": "",
            "top_items": [],
            "recommendations": []
        }

    return jsonify({
        "query": query,
        "report": report,
        "generated_at": datetime.utcnow().isoformat()
    })
