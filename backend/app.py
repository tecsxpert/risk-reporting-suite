from flask import Flask, request, jsonify
from flask_cors import CORS
import bleach
import re

app = Flask(__name__)
CORS(app)

def sanitize_input(user_input):
    return bleach.clean(user_input)


def detect_sql_injection(user_input):
    pattern = r"(select|insert|update|delete|drop|--|;)"
    return re.search(pattern, user_input.lower())

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()

        if not data or "input" not in data:
            return jsonify({"error": "No input provided"}), 400

        user_input = data["input"]

        # ✅ Length check
        if len(user_input) > 500:
            return jsonify({"error": "Input too long"}), 400

        
        if "<script>" in user_input.lower():
            return jsonify({"error": "Malicious script detected"}), 400

        if detect_sql_injection(user_input):
            return jsonify({"error": "SQL injection pattern detected"}), 400

       
        clean_input = sanitize_input(user_input)

        # 🤖 Simulated AI response
        response = {
            "original_input": user_input,
            "sanitized_input": clean_input,
            "analysis": "This is a placeholder risk analysis."
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)