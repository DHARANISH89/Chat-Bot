# 🎓 Student AI Chatbot

*A lightweight AI-powered chatbot for students built with Flask, SQLite, and a simple web interface.*

## 📌 Overview

The **Student AI Chatbot** is a minimal full-stack web application that allows students to interact with an AI assistant through a browser-based chat interface.

The system uses:

* **Flask** for the backend API
* **SQLite** for lightweight database storage
* **Vanilla JavaScript** for the frontend
* **OpenAI-compatible API support** for AI responses
* Optional **Hugging Face inference integration** via a proxy service

The application supports **chat history persistence, user authentication, and modular AI integration**, making it a good starting point for building larger AI-driven educational tools.

---

# 🚀 Features

### 💬 Chat System

* Real-time chat interface
* Timestamped messages
* Scrollable conversation history
* Persistent chat history stored in SQLite

### 🔐 User Authentication

* Simple **signup & login**
* Session-based authentication
* User-specific chat history

### 🤖 AI Integration

* Supports **OpenAI-compatible APIs**
* Optional **Hugging Face inference integration**
* Fallback **mock responses** if no API key is provided

### ⚙️ REST API Endpoints

| Endpoint       | Method | Description             |
| -------------- | ------ | ----------------------- |
| `/api/chat`    | POST   | Send message to chatbot |
| `/api/history` | GET    | Retrieve chat history   |
| `/signup`      | POST   | Register new user       |
| `/login`       | POST   | Authenticate user       |

---

# 🏗️ Project Architecture

```
student-ai-chatbot
│
├── app/
│   ├── routes.py        # API routes
│   ├── models.py        # Database models
│   ├── auth.py          # Authentication logic
│   └── database.db      # SQLite database
│
├── templates/
│   └── index.html       # Chat UI
│
├── static/
│   ├── css/
│   └── js/
│
├── llm_service.py       # HuggingFace proxy service
├── run.py               # Application entry point
├── requirements.txt
└── README.md
```

---

# ⚡ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/student-ai-chatbot.git
cd student-ai-chatbot
```

---

## 2️⃣ Create Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Set your OpenAI API key (optional).

### Windows

```powershell
$env:OPENAI_API_KEY="sk-..."
```

### Linux / Mac

```bash
export OPENAI_API_KEY="sk-..."
```

If no API key is provided, the chatbot returns **mock responses for testing**.

---

## 5️⃣ Run the Application

```bash
python run.py
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

---

# 🤖 Running the LLM Proxy Service (Optional)

The project includes **`llm_service.py`**, a lightweight Flask service that forwards requests to the **Hugging Face Inference API**.

This allows you to run **free or open-source LLMs instead of OpenAI**.

Run it in a separate terminal:

```bash
python llm_service.py
```

Then set:

```
LLM_SERVICE_URL=http://localhost:8000
```

The chatbot backend will send requests to this service.

---

# 💾 Database

The application uses **SQLite**, which requires no configuration.

The database stores:

* User accounts
* Chat messages
* Timestamps
* Conversation history

Example schema:

```
Users
-----
id
username
password_hash

Messages
--------
id
user_id
message
response
timestamp
```

---

# 🧪 Example API Request

```json
POST /api/chat

{
  "message": "Explain Newton's laws of motion"
}
```

Response:

```json
{
  "reply": "Newton's laws describe how objects move when forces act on them..."
}
```

---

# 🔒 Security Notes

This is a **minimal educational scaffold**. For production use, improvements should include:

* Password hashing with **bcrypt**
* **JWT authentication**
* **Rate limiting**
* **CSRF protection**
* Secure **session management**
* Input validation
* HTTPS with **HSTS**

---

# 📈 Future Improvements

Planned enhancements include:

* 🔹 Rate limiting per user
* 🔹 Token streaming responses
* 🔹 Conversation memory
* 🔹 Multi-model support
* 🔹 Docker deployment
* 🔹 Unit & integration tests
* 🔹 UI improvements (React frontend)
* 🔹 Role-based access control
* 🔹 RAG integration for study materials

---

# 🧑‍💻 Technologies Used

| Technology   | Purpose                |
| ------------ | ---------------------- |
| Flask        | Backend API            |
| SQLite       | Database               |
| JavaScript   | Frontend interaction   |
| OpenAI API   | AI responses           |
| Hugging Face | Optional LLM inference |
| Python       | Backend development    |

---

# 📚 Use Cases

This chatbot can be extended for:

* 📖 **Student study assistant**
* 🧠 **AI tutoring systems**
* 📑 **Course Q&A systems**
* 📊 **Educational dashboards**
* 🤖 **Campus AI helpdesk**

---

# 📄 License

This project is intended for **educational and experimental purposes**.

You may modify and distribute it under the **MIT License**.

---
