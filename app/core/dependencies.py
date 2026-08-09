from app.database.database import get_session

from app.services.message import MessageService
from app.repositories.sql_model.message import SqlModelMessageRepository

from app.services.role import RoleModel
from app.repositories.sql_model.role import SqlModelRoleRepository

from sqlmodel import Session
from fastapi import Depends

def get_message_repository(session: Session = Depends(get_session)):
    return SqlModelMessageRepository(session)

def get_message_service(repo: MessageService = Depends(get_message_repository)):
    return MessageService(repo)

def get_role_repository(session: Session = Depends(get_session)):
    return SqlModelRoleRepository(session)

def get_role_service(repo: MessageService = Depends(get_role_repository)):
    return RoleModel(repo)