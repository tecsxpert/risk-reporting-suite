from flask import Flask, request, jsonify
from flask_cors import CORS
import bleach
import re
from pymongo import MongoClient
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

username = quote_plus(os.getenv("MONGO_USERNAME", "ApoorvaBiradar"))
password = quote_plus(os.getenv("MONGO_PASSWORD", "appu@1214"))

MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.dpebjbj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["risk_reporting_db"]
collection = db["reports"]


# Sanitize Input
def sanitize_input(user_input):
    return bleach.clean(user_input)

# Detect SQL Injection
def detect_sql_injection(user_input):
    pattern = r"(select|insert|update|delete|drop|--|;|union|xp_)"
    return re.search(pattern, user_input.lower())

# Calculate Risk
def calculate_risk(user_input):
    text = user_input.lower()

    high_risk_keywords = [
        "fraud",
        "attack",
        "hack",
        "unauthorized",
        "phishing",
        "password leak",
        "credit card",
        "bank details",
        "otp",
        "ssn",
        "breach"
    ]

    medium_risk_keywords = [
        "error",
        "warning",
        "suspicious",
        "unknown login",
        "failed attempt",
        "alert"
    ]

    for word in high_risk_keywords:
        if word in text:
            return "HIGH"

    for word in medium_risk_keywords:
        if word in text:
            return "MEDIUM"

    return "LOW"

# Risk Score
def risk_score(risk_level):
    scores = {
        "HIGH": 90,
        "MEDIUM": 60,
        "LOW": 20
    }
    return scores.get(risk_level, 0)

# Analysis Message
def generate_analysis(risk_level):
    if risk_level == "HIGH":
        return "⚠️ High risk detected. Possible fraud or security threat."
    elif risk_level == "MEDIUM":
        return "⚠️ Medium risk detected. Suspicious activity found."
    else:
        return "✅ Low risk detected. System appears safe."


@app.route('/')
def home():
    return "Risk Reporting API is running successfully!"


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
        score = risk_score(risk_level)
        analysis = generate_analysis(risk_level)

        response = {
            "original_input": user_input,
            "sanitized_input": clean_input,
            "risk_level": risk_level,
            "score": score,
            "analysis": analysis
        }

        collection.insert_one(response)
        response.pop("_id", None)  # ✅ Fix: remove ObjectId added by MongoDB

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reports', methods=['GET'])
def get_reports():
    try:
        reports = []

        for report in collection.find({}, {"_id": 0}):
            reports.append(report)

        return jsonify(reports), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)