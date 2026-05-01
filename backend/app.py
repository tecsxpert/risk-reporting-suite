from flask import Flask, request, jsonify
from flask_cors import CORS
import bleach
import re

app = Flask(__name__)
CORS(app)



def sanitize_input(user_input):
    return bleach.clean(user_input)


def detect_sql_injection(user_input):
    pattern = r"(select|insert|update|delete|drop|--|;|union|xp_)"
    return re.search(pattern, user_input.lower())


def calculate_risk(user_input):
    text = user_input.lower()

    if "fraud" in text or "attack" in text:
        return "HIGH"
    elif "error" in text or "warning" in text:
        return "MEDIUM"
    else:
        return "LOW"


@app.route('/')
def home():
    return " Risk Reporting API is running successfully!"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()

        
        if not data or "input" not in data:
            return jsonify({"error": "No input provided"}), 400

        user_input = data["input"]

        if len(user_input) > 500:
            return jsonify({"error": "Input too long"}), 400

        if "<script>" in user_input.lower():
            return jsonify({"error": "Malicious script detected"}), 400

        if detect_sql_injection(user_input):
            return jsonify({"error": "SQL injection pattern detected"}), 400

        
        clean_input = sanitize_input(user_input)

       
        risk_level = calculate_risk(user_input)

      
        response = {
            "original_input": user_input,
            "sanitized_input": clean_input,
            "risk_level": risk_level,
            "analysis": f"{risk_level} risk detected based on input analysis"
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)