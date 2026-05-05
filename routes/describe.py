from flask import Blueprint, request, jsonify
from datetime import datetime
from services.prompts import PRIMARY_PROMPT
from services.llm_client import call_llm

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/", methods=["POST"])
def describe():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    prompt = PRIMARY_PROMPT.format(text=text)

    try:
        refined_output = call_llm(prompt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "description": refined_output,
        "generated_at": datetime.utcnow().isoformat()
    })