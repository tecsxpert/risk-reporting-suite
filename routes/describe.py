import re

from flask import Blueprint, request, jsonify
from services.llm_client import call_llm
from services.db import collection, model

describe_bp = Blueprint("describe", __name__)

def _parse_risk_and_impact(text):
    risk_match = re.search(r"risk:\s*(.+?)(?=\n|impact:|$)", text, re.IGNORECASE | re.DOTALL)
    impact_match = re.search(r"impact:\s*(.+?)(?=\n|risk:|$)", text, re.IGNORECASE | re.DOTALL)

    risk = risk_match.group(1).strip() if risk_match else None
    impact = impact_match.group(1).strip() if impact_match else None

    return risk, impact


@describe_bp.route("/", methods=["POST"])
def describe():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    try:
        refined_output = call_llm(text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    risk, impact = _parse_risk_and_impact(refined_output)

    if not risk or not impact:
        return jsonify({
            "error": "Output format invalid",
            "raw": refined_output
        }), 500

    description = " ".join(line.strip() for line in refined_output.splitlines() if line.strip())
    embedding = model.encode(text).tolist()
    doc_id = f"{text[:10]}_{len(text)}"
    collection.add(documents=[text], embeddings=[embedding], ids=[doc_id])

    return jsonify({
        "description": description,
        "risk": risk,
        "impact": impact
    })