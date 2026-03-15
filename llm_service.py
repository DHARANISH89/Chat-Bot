import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv()

app = Flask(__name__)

# --------------------------------------------------------------------
# Mistral API helper
# --------------------------------------------------------------------
def call_mistral_model(prompt, model=None, mistral_key=None, history=None):
    """
    Call Mistral's chat completion API and return the generated text.
    """
    mistral_key = mistral_key or os.getenv("MISTRAL_API_KEY")
    if not mistral_key:
        return None, "(LLM service) missing MISTRAL_API_KEY"

    model = model or os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {mistral_key}",
        "Content-Type": "application/json"
    }

    # Build the conversation in Mistral’s expected format
    messages = []
    if history:
        for msg in history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"], None
        return None, f"(Mistral API error) {r.status_code}: {r.text}"
    except Exception as e:
        return None, f"(Mistral request failed) {e}"


# --------------------------------------------------------------------
# API endpoints
# --------------------------------------------------------------------
@app.route("/generate", methods=["POST"])
def generate():
    body = request.json or {}
    prompt = body.get("prompt") or body.get("message") or ""
    history = body.get("history") or []
    model = body.get("model") or os.getenv("MISTRAL_MODEL")

    if not prompt:
        return jsonify({"error": "prompt required"}), 400

    text, err = call_mistral_model(prompt, model=model, history=history)
    if err:
        return jsonify({"error": err}), 502

    return jsonify({"generated_text": text})


@app.route("/health", methods=["GET"])
def health():
    mistral_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_key:
        return jsonify({"status": "missing_key"})
    return jsonify({"status": "ok", "provider": "mistral"})


@app.route("/", methods=["GET"])
def root():
    return jsonify({"service": "llm_service", "status": "running"})


@app.route("/discover", methods=["GET"])
def discover_models():
    """
    Try a short list of Mistral models and report which ones respond.
    """
    mistral_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_key:
        return jsonify({"status": "missing_key"})

    candidates = os.getenv(
        "MISTRAL_DISCOVER_MODELS",
        "mistral-tiny-latest,mistral-small-latest,mistral-medium-latest"
    ).split(",")

    results = {}
    for m in map(str.strip, candidates):
        if not m:
            continue
        _, err = call_mistral_model("Ping", model=m, mistral_key=mistral_key)
        results[m] = "ok" if err is None else f"error: {err}"

    return jsonify({"status": "done", "results": results})


# --------------------------------------------------------------------
# Main entry point
# --------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("LLM_SERVICE_PORT", "5001"))
    app.run(host="127.0.0.1", port=port, debug=True)
