from sqlmodel import SQLModel

class RoleSchema(SQLModel):
    name: str
