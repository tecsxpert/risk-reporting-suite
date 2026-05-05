from flask import Flask, request, jsonify
from services.sanitizer import sanitize_input, SanitizationError

app = Flask(__name__)

@app.route('/describe', methods=['POST'])
def describe_risk():
    data = request.get_json()
    user_text = data.get('text', '')
    try:
        safe_text = sanitize_input(user_text)
        return jsonify({"status": "success", "safe_text": safe_text}), 200
    except SanitizationError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
