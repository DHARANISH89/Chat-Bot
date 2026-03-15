import os
from dotenv import load_dotenv
from app import create_app

# ------------------------------------------------------------
# 1️⃣ Load environment variables
# ------------------------------------------------------------
# Automatically load variables from your .env file
# (Make sure .env is in the project root)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# ------------------------------------------------------------
# 2️⃣ Create the Flask app
# ------------------------------------------------------------
app = create_app()

# ------------------------------------------------------------
# 3️⃣ Print diagnostic info (useful for debugging)
# ------------------------------------------------------------
print("\n=== Flask App Configuration ===")
print(f"Environment file loaded from: {dotenv_path}")
print(f"LLM Provider: {os.getenv('LLM_PROVIDER')}")
print(f"Mistral Model: {os.getenv('MISTRAL_MODEL')}")
print(f"Mistral API Key Loaded: {'✅ Yes' if os.getenv('MISTRAL_API_KEY') else '❌ No'}")
print(f"LLM Service Port: {os.getenv('LLM_SERVICE_PORT', '5001')}")
print("=================================\n")

# ------------------------------------------------------------
# 4️⃣ Run the Flask app
# ------------------------------------------------------------
if __name__ == '__main__':
    # Default Flask runs on port 5000
    app.run(debug=True, host="127.0.0.1", port=5000)
