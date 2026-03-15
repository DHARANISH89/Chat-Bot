# Student AI Chatbot (Flask + SQLite)

Minimal web app that provides a chat interface for students to interact with an AI assistant. Built with Flask for the backend and vanilla JS for the frontend. Uses SQLite for storage and supports OpenAI-compatible API integration via environment variable.

Features:
- Chat interface with timestamps and scrollable history
- /api/chat and /api/history endpoints
- Simple user signup/login (session-based)

Quick start (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
$env:OPENAI_API_KEY = "sk-..."  # optional
python run.py
# open http://127.0.0.1:5000 in browser
```

Notes:
- If no OpenAI API key is provided, the server returns canned responses for testing.
- This is a minimal scaffold. See TODOs in the project for enhancements (rate limiting, better auth, tests).

---

Running a separate LLM service (recommended)
-----------------------------------------
The repository includes `llm_service.py` — a small Flask service that proxies requests to the Hugging Face Inference API. Run it in a separate terminal and point the main app to it with `LLM_SERVICE_URL`.

Committing files
----------------
To ensure all new files are committed (including `llm_service.py`), run:

```powershell
git add -A
git commit -m "Add LLM service and HF integration"
git push
```

