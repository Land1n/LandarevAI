from app.database.database import get_session

from app.services.message import MessageService
from app.repositories.sql_model.message import SqlModelMessageRepository,MessageRepository

from app.services.role import RoleService
from app.repositories.sql_model.role import SqlModelRoleRepository,RoleRepository

from sqlmodel import Session
from fastapi import Depends

def get_message_repository(session: Session = Depends(get_session)):
    return SqlModelMessageRepository(session)

def get_role_repository(session: Session = Depends(get_session)):
    return SqlModelRoleRepository(session)

def get_message_service(
        message_repo: MessageRepository = Depends(get_message_repository),
        role_repo: RoleRepository = Depends(get_role_repository)
):
    return MessageService(message_repo,role_repo)

def get_role_service(repo: RoleService = Depends(get_role_repository)):
     return RoleService(repo)