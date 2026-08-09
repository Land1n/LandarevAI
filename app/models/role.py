from __future__ import annotations

from app.schemas.role import RoleSchema
from sqlmodel import Field

from typing import Optional

class RoleModel(RoleSchema,table=True):
    __tablename__ = 'role'
    id: Optional[int] = Field(default=None, primary_key=True)