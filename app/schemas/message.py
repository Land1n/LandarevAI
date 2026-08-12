from typing import Optional

from datetime import time,datetime

from sqlmodel import SQLModel

def current_time() -> time:
    return datetime.now().time()

class MessageShema(SQLModel):
    text:str
    role_name: str
