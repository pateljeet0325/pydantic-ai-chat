from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from tools.calculator import calculator

from tools.database_tool import list_chat_sessions
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL")
)

tools = [
    calculator,
    list_chat_sessions
]

agent = create_react_agent(
    llm,
    tools,
    prompt="""
You are a helpful AI assistant.

Use the calculator tool for mathematical calculations.

Use the list_chat_sessions tool when the user asks
about saved chats, chat sessions, or stored conversations.

Present tool results directly.
""")

def chat_with_agent(
    message: str,
    history: list = None
):

    messages = []

    if history:
        messages.extend(history)

    messages.append(
        ("user", message)
    )

    response = agent.invoke(
        {
            "messages": messages
        }
    )
    print(response)

    return response["messages"][-1].content