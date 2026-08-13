from typing import Optional, TYPE_CHECKING
from datetime import time, datetime

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Time

from app.schemas.message import MessageShema


if TYPE_CHECKING:
    from app.models.role import RoleModel

def current_time() -> time:
    return datetime.now().time()

class MessageModel(MessageShema, table=True):
    __tablename__ = "message"

    id: Optional[int] = Field(default=None, primary_key=True)

    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional["RoleModel"] = Relationship(back_populates="messages")

    created_at_time: time = Field(default_factory=current_time, sa_type=Time)