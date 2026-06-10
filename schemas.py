from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    title: str

from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    model: str

from pydantic import BaseModel

class RenameSessionRequest(BaseModel):
    title: str