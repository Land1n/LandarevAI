from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

from app.schemas.role import RoleSchema

if TYPE_CHECKING:
    from app.models.message import MessageModel


class RoleModel(RoleSchema, table=True):
    __tablename__ = "role"

    id: Optional[int] = Field(default=None, primary_key=True)

    messages: List["MessageModel"] = Relationship(back_populates="role")