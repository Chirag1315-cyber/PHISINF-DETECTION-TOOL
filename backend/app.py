from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import joblib

app = Flask(__name__)
CORS(app)

# -----------------------------
# Load ML model (optional)
# -----------------------------
try:
    model = joblib.load("phishing_model.pkl")
    MODEL_LOADED = True
    print("Model loaded successfully")
except:
    model = None
    MODEL_LOADED = False
    print("Model not found, using heuristic rules")

# -----------------------------
# Helper Functions
# -----------------------------
def heuristic_check(url: str) -> bool:
    """
    Simple phishing indicators
    """
    if "@" in url:
        return True
    if "-" in url:
        return True
    if re.search(r"\d{4,}", url):
        return True
    return False


def extract_features(url: str):
    """
    Feature vector for ML model
    """
    return [
        len(url),
        url.count("."),
        url.count("-"),
        int("@" in url)
    ]

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "model_loaded": MODEL_LOADED
    })


@app.route("/api/check_url", methods=["POST"])
def check_url():
    # Validate JSON
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "URL is required"}), 400

    verdict = "safe"
    score = 0.1
    method = "heuristic"

    # ML-based detection
    if MODEL_LOADED:
        try:
            features = extract_features(url)
            prediction = model.predict([features])[0]
            verdict = "phishing" if prediction == 1 else "safe"
            score = 0.9 if verdict == "phishing" else 0.1
            method = "ml-model"
        except Exception as e:
            print("Model error:", e)

    # Heuristic fallback
    else:
        if heuristic_check(url):
            verdict = "suspicious"
            score = 0.6

    return jsonify({
        "url": url,
        "verdict": verdict,
        "confidence": score,
        "detection_method": method
    })

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
