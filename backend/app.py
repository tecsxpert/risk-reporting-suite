from flask import Flask, request, jsonify
from flask_cors import CORS
import bleach
import re
from pymongo import MongoClient
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import bcrypt
import jwt
import datetime
from functools import wraps

# ==============================
# Load Environment Variables
# ==============================
load_dotenv()

# ==============================
# Flask App Setup
# ==============================
app = Flask(__name__)
CORS(app)

# Secret Key
app.config['SECRET_KEY'] = 'supersecretkey'

# ==============================
# MongoDB Connection
# ==============================
username = quote_plus(os.getenv("MONGO_USERNAME", "ApoorvaBiradar"))
password = quote_plus(os.getenv("MONGO_PASSWORD", "appu@1214"))

MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.dpebjbj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["risk_reporting_db"]

# Collections
reports_collection = db["reports"]
users_collection = db["users"]

# ==============================
# Helper Functions
# ==============================

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

# Generate Analysis
def generate_analysis(risk_level):

    if risk_level == "HIGH":
        return "⚠️ High risk detected. Possible fraud or security threat."

    elif risk_level == "MEDIUM":
        return "⚠️ Medium risk detected. Suspicious activity found."

    else:
        return "✅ Low risk detected. System appears safe."

# ==============================
# JWT FUNCTIONS
# ==============================

# Generate JWT Token
def generate_token(username):

    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return token

# Token Verification
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        # Read Token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        # No Token
        if not token:

            return jsonify({
                "error": "Token is missing"
            }), 401

        try:

            # Decode Token
            data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )

            current_user = data['username']

        except:

            return jsonify({
                "error": "Invalid or expired token"
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated

# ==============================
# Routes
# ==============================

# Home Route
@app.route('/')
def home():

    return "Risk Reporting API is running successfully!"

# ==============================
# Analyze Route (Protected)
# ==============================
@app.route('/analyze', methods=['POST'])
@token_required
def analyze(current_user):

    try:

        data = request.get_json()

        if not data or "input" not in data:

            return jsonify({
                "error": "No input provided"
            }), 400

        user_input = data["input"]

        # Input Length Check
        if len(user_input) > 500:

            return jsonify({
                "error": "Input too long"
            }), 400

        # Script Detection
        if "<script>" in user_input.lower():

            return jsonify({
                "error": "Malicious script detected"
            }), 400

        # SQL Injection Detection
        if detect_sql_injection(user_input):

            return jsonify({
                "error": "SQL injection pattern detected"
            }), 400

        # Sanitize Input
        clean_input = sanitize_input(user_input)

        # Risk Logic
        risk_level = calculate_risk(user_input)

        # Score
        score = risk_score(risk_level)

        # Analysis
        analysis = generate_analysis(risk_level)

        # Response Object
        response = {
            "username": current_user,
            "original_input": user_input,
            "sanitized_input": clean_input,
            "risk_level": risk_level,
            "score": score,
            "analysis": analysis
        }

        # Save Report
        reports_collection.insert_one(response)

        return jsonify(response), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# ==============================
# Reports Route (Protected)
# ==============================
@app.route('/reports', methods=['GET'])
@token_required
def get_reports(current_user):

    try:

        reports = []

        for report in reports_collection.find(
            {"username": current_user},
            {"_id": 0}
        ):

            reports.append(report)

        return jsonify(reports), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# ==============================
# Register Route
# ==============================
@app.route('/register', methods=['POST'])
def register():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:

            return jsonify({
                "error": "Username and password required"
            }), 400

        existing_user = users_collection.find_one({
            "username": username
        })

        if existing_user:

            return jsonify({
                "error": "User already exists"
            }), 400

        # Hash Password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )

        # Save User
        users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# ==============================
# Login Route
# ==============================
@app.route('/login', methods=['POST'])
def login():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = users_collection.find_one({
            "username": username
        })

        # User Not Found
        if not user:

            return jsonify({
                "error": "Invalid username"
            }), 401

        # Password Check
        if bcrypt.checkpw(
            password.encode('utf-8'),
            user["password"]
        ):

            token = generate_token(username)

            return jsonify({
                "message": "Login successful",
                "token": token
            }), 200

        return jsonify({
            "error": "Invalid password"
        }), 401

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# ==============================
# Run App
# ==============================
if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )