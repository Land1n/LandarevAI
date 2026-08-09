from __future__ import annotations

from app.schemas.message import MessageShema
from sqlmodel import Field

from typing import Optional

class MessageModel(MessageShema,table=True):
    __tablename__ = 'message'
    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: Optional[int] =  Field(default=None, foreign_key="role.id")