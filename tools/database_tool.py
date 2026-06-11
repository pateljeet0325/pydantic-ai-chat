from langchain.tools import tool

from database import SessionLocal
from models import ChatSession


@tool
def list_chat_sessions() -> str:
    """
    List all chat sessions stored in the PostgreSQL database.
    Use this tool whenever the user asks:
    - list chat sessions
    - show chat sessions
    - show chats
    - what chats exist
    - display saved sessions
    """

    db = SessionLocal()

    sessions = db.query(ChatSession).all()

    db.close()

    if not sessions:
        return "No chat sessions found."

    return "\n".join(
        [session.title for session in sessions]
    )