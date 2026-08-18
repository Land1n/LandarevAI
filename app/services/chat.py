# app/services/chat.py
from typing import Optional, List
import logging

from app.repositories.base.chat import ChatRepository, ChatModel
from app.repositories.base.message import MessageRepository, MessageModel
from app.repositories.base.role import RoleRepository
from app.core.logger.logger import convert_result, logger
from app.core.logger.schemas.answer import Answer


class ChatService:
    def __init__(self, chat_repository: ChatRepository,
                 message_repository: MessageRepository,
                 role_repository: RoleRepository):
        self.chat_repository = chat_repository
        self.message_repository = message_repository
        self.role_repository = role_repository

    @convert_result
    @logger("ChatService")
    def delete_all_chats(self) -> bool:
        try:
            chats = self.chat_repository.read_all()
            for chat in chats:
                for msg in chat.messages:
                    self.message_repository.delete(msg.id)
                self.chat_repository.delete(chat.id)
            return Answer[ChatModel](result=True, level=logging.INFO)
        except Exception as e:
            return Answer[ChatModel](result=False, level=logging.ERROR, description=str(e))
    @convert_result
    @logger("ChatService")
    def list_chats(self) -> List[ChatModel]:
        try:
            chats = self.chat_repository.read_all()
            return Answer[ChatModel](result=chats, level=logging.INFO)
        except Exception as e:
            return Answer[ChatModel](result=[], level=logging.ERROR, description=str(e))

    @convert_result
    @logger("ChatService")
    def read_chat_by_id(self, id: int) -> Optional[ChatModel]:
        try:
            chat = self.chat_repository.read_by_id(id)
            if chat:
                return Answer[ChatModel](result=chat, level=logging.INFO)
            return Answer[ChatModel](
                result=None,
                level=logging.WARNING,
                description=f"Chat with id={id} not found"
            )
        except Exception as e:
            return Answer[ChatModel](result=None, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("ChatService")
    def create_chat(self, chat: ChatModel) -> bool:
        try:
            is_created = self.chat_repository.create(chat)
            return Answer[ChatModel](result=is_created, level=logging.INFO)
        except Exception as e:
            return Answer[ChatModel](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("ChatService")
    def update_chat(self, id: int, chat: ChatModel) -> bool:
        try:
            old_chat = self.chat_repository.read_by_id(id)
            if old_chat is None:
                return Answer[ChatModel](
                    result=False,
                    level=logging.ERROR,
                    description=f"Chat with id={id} not found"
                )
            is_updated = self.chat_repository.update(id, chat)
            if not is_updated:
                return Answer[ChatModel](
                    result=is_updated,
                    level=logging.WARNING,
                    description="Update returned False"
                )
            return Answer[ChatModel](result=is_updated, level=logging.INFO)
        except Exception as e:
            return Answer[ChatModel](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("ChatService")
    def delete_chat(self, id: int) -> bool:
        try:
            old_chat = self.chat_repository.read_by_id(id)
            if old_chat is None:
                return Answer[ChatModel](
                    result=False,
                    level=logging.ERROR,
                    description=f"Chat with id={id} not found"
                )
            is_deleted = self.chat_repository.delete(id)
            if not is_deleted:
                return Answer[ChatModel](
                    result=is_deleted,
                    level=logging.WARNING,
                    description="Delete returned False"
                )
            return Answer[ChatModel](result=is_deleted, level=logging.INFO)
        except Exception as e:
            return Answer[ChatModel](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("ChatService")
    def add_message_to_chat(self, chat_id: int, message: MessageModel) -> bool:
        try:
            chat_ans = self.chat_repository.read_by_id(chat_id)
            if chat_ans is None:
                return Answer[MessageModel](
                    result=False,
                    level=logging.ERROR,
                    description=f"Chat with id={chat_id} not found"
                )

            message.chat_id = chat_ans.id

            if hasattr(message, 'role_name') and message.role_name and message.role_id is None:
                role_ans = self.role_repository.read_by_name(message.role_name)
                if role_ans is None:
                    return Answer[MessageModel](
                        result=False,
                        level=logging.ERROR,
                        description=f"Role '{message.role_name}' not found"
                    )
                message.role_id = role_ans.id

            created = self.message_repository.create(message)
            if not created:
                return Answer[MessageModel](
                    result=False,
                    level=logging.WARNING,
                    description="Message creation failed"
                )
            return Answer[MessageModel](result=True, level=logging.INFO)
        except Exception as e:
            return Answer[MessageModel](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("ChatService")
    def set_model_for_chat(self, chat_id: int, model_id: int) -> bool:
        """Устанавливает модель для чата."""
        chat = self.chat_repository.read_by_id(chat_id)
        if not chat:
            return Answer[ChatModel](result=False, level=logging.ERROR, description=f"Chat {chat_id} not found")
        chat.model_id = model_id
        return self.update_chat(chat_id, chat)