from typing import Optional
from sqlmodel import Field, SQLModel
from app.schemas.ai_model import AIModelSchema

class AIModel(AIModelSchema, table=True):
    __tablename__ = "ai_model"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(nullable=False)