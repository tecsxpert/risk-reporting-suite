from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from services.sanitizer import sanitize_input, SanitizationError

app = Flask(__name__)

# DAY 8 FIX: Add security headers automatically (Fixes ZAP Medium findings)
Talisman(app, force_https=False)

# Setup rate limiter (Default: 30 req/min globally)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["30 per minute"]
)

@app.route('/describe', methods=['POST'])
def describe_risk():
    data = request.get_json()
    user_text = data.get('text', '')
    try:
        safe_text = sanitize_input(user_text)
        return jsonify({"status": "success", "safe_text": safe_text}), 200
    except SanitizationError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/generate-report', methods=['POST'])
@limiter.limit("10 per minute") 
def generate_report():
    data = request.get_json()
    user_text = data.get('text', '')
    try:
        safe_text = sanitize_input(user_text)
        return jsonify({"status": "success", "message": "Report generation started"}), 200
    except SanitizationError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
