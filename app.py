from flask import Flask
from routes.describe import describe_bp
from routes.recommend import recommend_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(describe_bp, url_prefix="/describe")
app.register_blueprint(recommend_bp, url_prefix="/recommend")

@app.route("/")
def home():
    return "✅ Risk Reporting AI Service is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
