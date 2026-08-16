from typing import List, Optional
from sqlmodel import SQLModel

class ChatShema(SQLModel):
    name: str

class ChatResponse(ChatShema):
    messages: List['MessageShema']

class ChatCreateResponse(ChatShema):
    id: int