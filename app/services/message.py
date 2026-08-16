from app.repositories.base.message import MessageRepository, MessageModel
from app.repositories.base.role import RoleRepository

from app.core.logger.logger import logger,convert_result

from typing import List,Optional

import logging

from app.core.logger.schemas.answer import Answer


class MessageService:

    def __init__(self, message_repository: MessageRepository,role_repository:RoleRepository) -> None:
        self.message_repository = message_repository
        self.role_repository = role_repository

    @convert_result
    @logger("MessageService")
    def list_messages(self) -> List[MessageModel]:
        try:
            data = self.message_repository.read_all()
            return Answer[MessageModel](result=data, level=logging.INFO)
        except Exception as e:
            return Answer[MessageModel](result=[],level=logging.ERROR,description=str(e))

    @convert_result
    @logger("MessageService")
    def list_messages_by_role(self, role: str) -> List[MessageModel]:
        try:
            messages = self.message_repository.read_by_role(role)
            return Answer[MessageModel](result=messages, level=logging.INFO)
        except Exception as e:
            return Answer[MessageModel](result=[],level=logging.ERROR,description=str(e))


    @convert_result
    @logger("MessageService")
    def read_message(self, message_id: int) -> Optional[MessageModel]:
        try:
            message = self.message_repository.read_by_id(message_id)
            if message:
                return Answer[MessageModel](result=message, level=logging.INFO)
            return Answer[MessageModel](result=message,level=logging.WARNING,description=f"{message=}")

        except Exception as e:
            return Answer[MessageModel](result=None,level=logging.ERROR,description=str(e))

    @convert_result
    @logger("MessageService")
    def create_message(self, message: MessageModel) -> bool:
        try:
            if message.role_name:
                role = self.role_repository.read_by_name(message.role_name)
                if role is None:
                    return Answer[MessageModel](result=False,level=logging.ERROR,description=f"{role=}")
                message.role = role
                is_created = self.message_repository.create(message)
                return Answer[MessageModel](result=is_created)
            return Answer[MessageModel](result=False,level=logging.ERROR,description=f"{message.role_name=}")
        except Exception as e:
            return Answer[MessageModel](result=False,level=logging.ERROR,description=str(e))

    @convert_result
    @logger("MessageService")
    def update_message(self, message_id: int, new_message: MessageModel) -> bool:
        try:
            old_message = self.message_repository.read_by_id(message_id)
            if not old_message:
                return Answer[MessageModel](result=False,level=logging.ERROR,description=f"{old_message=}")
            if old_message.role != new_message.role and new_message.role is not None:
                return Answer[MessageModel](result=False,level=logging.ERROR,description=f"{old_message.role == new_message.role=}")
            old_message.text = new_message.text
            is_update = self.message_repository.update(message_id, old_message)
            if not is_update:
                return Answer[MessageModel](result=is_update, level=logging.WARNING,description=f"{is_update=}")
            return Answer[MessageModel](result=is_update, level=logging.INFO)
        except Exception as e:
            return Answer[MessageModel](result=False,level=logging.ERROR,description=str(e))

    @convert_result
    @logger("MessageService")
    def delete_message(self, message_id: int) -> bool:
        try:
            is_delete = self.message_repository.delete(id=message_id)
            if not is_delete:
                return Answer[MessageModel](result=is_delete,level=logging.WARNING,description=f"{is_delete=}")
            return Answer[MessageModel](result=is_delete, level=logging.INFO)
        except Exception as e:
            return Answer[MessageModel](result=False,level=logging.ERROR,description=str(e))