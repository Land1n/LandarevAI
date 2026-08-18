from typing import List, Optional
from sqlmodel import SQLModel
from app.schemas.message import MessageShema
from app.schemas.ai_model import AIModelSchema


class ChatShema(SQLModel):
    name: str
    model_id: Optional[int] = None

class ChatResponse(ChatShema):
    messages: List[MessageShema]
    model: AIModelSchema

class ChatCreateResponse(ChatShema):
    id: int