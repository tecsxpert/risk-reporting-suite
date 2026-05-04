from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
import bleach
import re
import os
import logging 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
CORS(app)


limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["30 per minute"]
)

Talisman(
    app,
    force_https=False,  # Keep False for local dev
    strict_transport_security=False,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self'",
        'style-src': "'self'",
        'img-src': "'self' data:",
        'connect-src': "'self'"
    },
    referrer_policy='strict-origin-when-cross-origin',
    permissions_policy={
        'geolocation': '()',
        'microphone': '()',
        'camera': '()'
    }
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def sanitize_input(user_input):
    return bleach.clean(user_input)


def detect_sql_injection(user_input):
    pattern = r"(select|insert|update|delete|drop|--|;|union|xp_)"
    return re.search(pattern, user_input.lower())


def detect_prompt_injection(user_input):
    """✅ Day 8 — Detect prompt injection patterns"""
    patterns = [
        r"ignore previous instructions",
        r"ignore above",
        r"disregard",
        r"you are now",
        r"act as",
        r"jailbreak",
        r"bypass",
        r"override instructions",
    ]
    for pattern in patterns:
        if re.search(pattern, user_input.lower()):
            return True
    return False


def detect_pii(user_input):
    """✅ Day 9 — Detect common PII patterns in input"""
    pii_patterns = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    }
    found = []
    for pii_type, pattern in pii_patterns.items():
        if re.search(pattern, user_input):
            found.append(pii_type)
    return found


def calculate_risk(user_input):
    text = user_input.lower()

    high_risk_keywords = [
        "fraud", "attack", "hack", "unauthorized",
        "phishing", "password leak", "credit card",
        "bank details", "otp", "ssn"
    ]

    medium_risk_keywords = [
        "error", "warning", "suspicious",
        "unknown login", "failed attempt"
    ]

    for word in high_risk_keywords:
        if word in text:
            return "HIGH"

    for word in medium_risk_keywords:
        if word in text:
            return "MEDIUM"

    return "LOW"


@app.route('/')
def home():
    return jsonify({"message": "Risk Reporting API is running successfully!"}), 200


@app.route('/health')
def health():
    """✅ Day 8 — Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ai-service"}), 200


@app.route('/analyze', methods=['POST'])
@limiter.limit("30 per minute")
def analyze():
    try:
        data = request.get_json()

        if not data or "input" not in data:
            return jsonify({"error": "No input provided"}), 400

        user_input = data["input"]

        # ✅ Day 9 — Log only length, never raw content
        logger.info(f"Analyze request received. Input length: {len(user_input)}")

        # Length check
        if len(user_input) > 500:
            return jsonify({"error": "Input too long. Maximum 500 characters allowed."}), 400

        # XSS check
        if "<script>" in user_input.lower():
            return jsonify({"error": "Malicious script detected"}), 400

        # SQL injection check
        if detect_sql_injection(user_input):
            return jsonify({"error": "SQL injection pattern detected"}), 400

        # ✅ Day 8 — Prompt injection check
        if detect_prompt_injection(user_input):
            return jsonify({"error": "Prompt injection pattern detected"}), 400

        # ✅ Day 9 — PII check
        pii_found = detect_pii(user_input)
        if pii_found:
            logger.warning(f"PII detected in input: {pii_found} (content not logged)")
            return jsonify({
                "error": f"Input contains sensitive personal information: {', '.join(pii_found)}. Please remove PII before submitting."
            }), 400

        # Sanitize
        clean_input = sanitize_input(user_input)

        # Risk calculation on sanitized input
        risk_level = calculate_risk(clean_input)

        response = {
            "original_input": user_input,
            "sanitized_input": clean_input,
            "risk_level": risk_level,
            "analysis": f"{risk_level} risk detected based on input analysis"
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in analyze endpoint: {type(e).__name__}")
        return jsonify({"error": str(e)}), 500
    


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)