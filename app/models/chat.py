from typing import Optional, TYPE_CHECKING,List
from datetime import time, datetime

from sqlmodel import Field, Relationship

from app.schemas.chat import ChatShema


if TYPE_CHECKING:
    from app.models.message import MessageModel

def current_time() -> time:
    return datetime.now().time()

class ChatModel(ChatShema, table=True):
    __tablename__ = "chat"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, nullable=False)
    messages: List["MessageModel"] = Relationship(back_populates="chat")

