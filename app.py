from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles



from pydantic_ai import Agent
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    UserPromptPart,
    TextPart,
)

from database import SessionLocal
from models import ChatSession, Message
from schemas import (
    CreateSessionRequest,
    ChatRequest,
    RenameSessionRequest
)

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")




def build_history(messages):
    history = []

    for msg in messages:

        if msg.role == "user":
            history.append(
                ModelRequest(
                    parts=[
                        UserPromptPart(
                            content=msg.content
                        )
                    ]
                )
            )

        elif msg.role == "assistant":
            history.append(
                ModelResponse(
                    parts=[
                        TextPart(
                            content=msg.content
                        )
                    ]
                )
            )

    return history


@app.get("/")
def home():
    return {
        "message": "PydanticAI Chat App"
    }


@app.post("/session")
def create_session(request: CreateSessionRequest):

    db = SessionLocal()

    session = ChatSession(
        title=request.title
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    db.close()

    return {
        "session_id": session.id,
        "title": session.title
    }


@app.post("/chat/{session_id}")
def chat(session_id: int, request: ChatRequest):

    db = SessionLocal()

    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if not session:
        db.close()
        return {
            "error": "Session not found"
        }

    previous_messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.id)
        .all()
    )

    history = build_history(previous_messages)

    dynamic_agent = Agent(
        f"groq:{request.model}"
    )

    result = dynamic_agent.run_sync(
        request.message,
        message_history=history
    )

    user_message = Message(
        session_id=session_id,
        role="user",
        content=request.message
    )

    assistant_message = Message(
        session_id=session_id,
        role="assistant",
        content=result.output
    )

    db.add(user_message)
    db.add(assistant_message)

    db.commit()
    db.close()

    return {
        "response": result.output
    }

@app.get("/sessions")
def get_sessions():

    db = SessionLocal()

    sessions = (
        db.query(ChatSession)
        .order_by(ChatSession.id.desc())
        .all()
    )

    result = []

    for session in sessions:
        result.append({
            "id": session.id,
            "title": session.title
        })

    db.close()

    return result

@app.get("/messages/{session_id}")
def get_messages(session_id: int):

    db = SessionLocal()

    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.id)
        .all()
    )

    result = []

    for message in messages:
        result.append({
            "role": message.role,
            "content": message.content
        })

    db.close()

    return result

@app.get("/ui")
def ui():
    return FileResponse("static/index.html")

@app.delete("/session/{session_id}")
def delete_session(session_id: int):

    db = SessionLocal()

    db.query(Message).filter(
        Message.session_id == session_id
    ).delete()

    db.query(ChatSession).filter(
        ChatSession.id == session_id
    ).delete()

    db.commit()
    db.close()

    return {
        "message": "Session deleted"
    }


@app.put("/session/{session_id}")
def rename_session(
    session_id: int,
    request: RenameSessionRequest
):

    db = SessionLocal()

    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if not session:
        db.close()
        return {
            "error": "Session not found"
        }

    session.title = request.title

    db.commit()
    db.close()

    return {
        "message": "Session renamed"
    }

@app.get("/models")
def get_models():

    return [
        {
            "id": "llama-3.3-70b-versatile",
            "name": "Llama 3.3 70B"
        },
        {
            "id": "deepseek-r1-distill-llama-70b",
            "name": "DeepSeek R1"
        },
        {
            "id": "gemma2-9b-it",
            "name": "Gemma 2 9B"
        }
    ]