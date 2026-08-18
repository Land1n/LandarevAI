from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from app.schemas.ai_model import AIModelSchema

if TYPE_CHECKING:
    from app.models.chat import ChatModel

class AIModel(AIModelSchema, table=True):
    __tablename__ = "ai_model"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(nullable=False)

    chats: List["ChatModel"] = Relationship(back_populates="model")