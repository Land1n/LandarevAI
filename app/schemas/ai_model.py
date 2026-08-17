from sqlmodel import SQLModel
from typing import Optional

class AIModelSchema(SQLModel):
    url: str