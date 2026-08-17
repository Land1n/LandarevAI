from app.database.database import get_session

from app.services.message import MessageService
from app.repositories.sql_model.message import SqlModelMessageRepository, MessageRepository

from app.services.role import RoleService
from app.repositories.sql_model.role import SqlModelRoleRepository, RoleRepository

from app.services.chat import ChatService
from app.repositories.sql_model.chat import SqlModelChatRepository, ChatRepository

from app.services.ai_model import AIModelService
from app.repositories.sql_model.ai_model import SqlModelAIModelRepository, AIModelRepository

from sqlmodel import Session
from fastapi import Depends

def get_message_repository(session: Session = Depends(get_session)):
    return SqlModelMessageRepository(session)

def get_role_repository(session: Session = Depends(get_session)):
    return SqlModelRoleRepository(session)

def get_chat_repository(session: Session = Depends(get_session)):
    return SqlModelChatRepository(session)

def get_message_service(
        message_repo: MessageRepository = Depends(get_message_repository),
        role_repo: RoleRepository = Depends(get_role_repository)
):
    return MessageService(message_repo, role_repo)

def get_role_service(repo: RoleRepository = Depends(get_role_repository)):
    return RoleService(repo)

def get_chat_service(
        chat_repo: ChatRepository = Depends(get_chat_repository),
        message_repo: MessageRepository = Depends(get_message_repository),
        role_repo: RoleRepository = Depends(get_role_repository)
):
    return ChatService(chat_repo, message_repo, role_repo)

def get_ai_model_repository(session: Session = Depends(get_session)):
    return SqlModelAIModelRepository(session)

def get_ai_model_service(
    repo: AIModelRepository = Depends(get_ai_model_repository)
):
    return AIModelService(repo)