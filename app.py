import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# Application + model versions are tracked independently (core MLOps idea).
# APP_VERSION can be overridden at build/deploy time; otherwise read VERSION file.
MODEL_VERSION = "model-7"


def read_app_version():
    # Prefer an env var injected at build time, else fall back to the VERSION file.
    version = os.environ.get("APP_VERSION")
    if version:
        return version.strip()
    try:
        with open(os.path.join(os.path.dirname(__file__), "VERSION")) as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"


def read_git_commit():
    # Set by the CI/CD build; unknown when running from source.
    return os.environ.get("GIT_COMMIT", "unknown")


@app.route("/")
def home():
    return jsonify({
        "service": "mlops-demo",
        "status": "running",
    })


@app.route("/health")
def health():
    return jsonify({
        "application_version": read_app_version(),
        "model_version": MODEL_VERSION,
        "git_commit": read_git_commit(),
        "status": "healthy",
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    value = float(data["value"])
    # Dummy ML prediction for teaching purposes.
    prediction = value * 2
    return jsonify({
        "input": value,
        "prediction": prediction,
        "model_version": MODEL_VERSION,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
