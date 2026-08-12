from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

from app.schemas.message import MessageShema

if TYPE_CHECKING:
    from app.models.role import RoleModel


class MessageModel(MessageShema, table=True):
    __tablename__ = "message"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")

    role: Optional["RoleModel"] = Relationship(back_populates="messages")