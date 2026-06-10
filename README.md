# PydanticAI Multi-Session Chat Application

## Project Overview

This project is a web-based AI chat application built using **PydanticAI**, **FastAPI**, **Groq**, and **PostgreSQL**.

The application supports multiple chat sessions, persistent conversation history, model selection, session management, and memory retention across browser refreshes and server restarts.

Each chat session is stored in PostgreSQL and can be reopened later with its complete conversation history.

---

# Features

## AI Chat

* Send messages to AI models using Groq.
* Receive intelligent responses from selected models.
* Supports conversation memory within each session.

## Multi-Session Support

* Create multiple chat sessions.
* Switch between conversations.
* Maintain separate memory for each session.

Example:

Chat 1:

* Python Learning

Chat 2:

* AI Agent Project

Chat 3:

* Interview Preparation

Each chat remembers its own conversation history.

## Persistent Memory

Conversation history is stored in PostgreSQL.

Memory is not lost when:

* Browser is refreshed
* FastAPI server is restarted
* User switches sessions

## Session Management

Users can:

* Create sessions
* Rename sessions
* Delete sessions
* Load previous conversations

## Dynamic Model Selection

Users can select different Groq models before sending messages.

Supported Models:

* Llama 3.3 70B
* DeepSeek R1
* Gemma 2 9B

Models are loaded dynamically from the backend.

## Chat Interface

Frontend includes:

* Sidebar for chat sessions
* Chat history window
* Message input
* Model selector
* Send button

---

# Technology Stack

## Backend

* FastAPI
* PydanticAI
* SQLAlchemy
* PostgreSQL

## AI Models

* Groq API

## Frontend

* HTML
* CSS
* JavaScript

## Database

* PostgreSQL

---

# Project Architecture

Frontend
(HTML/CSS/JavaScript)

↓

FastAPI Backend

↓

PydanticAI Agent

↓

Groq Models

↓

PostgreSQL Database

---

# Folder Structure

```text
pydantic-ai-chat/
│
├── app.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── .env
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

# Database Schema

## chat_sessions

Stores chat session information.

Fields:

* id
* title

Example:

| id | title            |
| -- | ---------------- |
| 1  | Python Learning  |
| 2  | AI Agent Project |

---

## messages

Stores all chat messages.

Fields:

* id
* session_id
* role
* content
* created_at

Example:

| session_id | role      | content         |
| ---------- | --------- | --------------- |
| 1          | user      | What is Python? |
| 1          | assistant | Python is...    |

---

# API Endpoints

## Create Session

POST /session

Request:

```json
{
  "title": "Python Learning"
}
```

Response:

```json
{
  "session_id": 1,
  "title": "Python Learning"
}
```

---

## Get All Sessions

GET /sessions

Response:

```json
[
  {
    "id": 1,
    "title": "Python Learning"
  }
]
```

---

## Send Message

POST /chat/{session_id}

Request:

```json
{
  "message": "What is Python?",
  "model": "llama-3.3-70b-versatile"
}
```

Response:

```json
{
  "response": "Python is a programming language..."
}
```

---

## Get Session Messages

GET /messages/{session_id}

Response:

```json
[
  {
    "role": "user",
    "content": "What is Python?"
  },
  {
    "role": "assistant",
    "content": "Python is..."
  }
]
```

---

## Rename Session

PUT /session/{session_id}

Request:

```json
{
  "title": "AI Agent Project"
}
```

---

## Delete Session

DELETE /session/{session_id}

---

## Get Available Models

GET /models

Response:

```json
[
  {
    "id": "llama-3.3-70b-versatile",
    "name": "Llama 3.3 70B"
  }
]
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd pydantic-ai-chat
```

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Create PostgreSQL Database

Create database:

```sql
CREATE DATABASE chat_app;
```

Update database connection settings in:

```python
database.py
```

---

## Run Application

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000/ui
```

---

# Future Enhancements

* Streaming responses
* Authentication
* User accounts
* Export chat history
* File uploads
* RAG integration
* Dark/Light theme
* Docker deployment

---

# Author

Jeet Patel

B.Tech Computer Science Engineering

Built using PydanticAI, FastAPI, Groq, and PostgreSQL.
url="http://127.0.0.1:8000/ui"