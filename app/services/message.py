from sqlalchemy.sql.dml import isdelete

from app.repositories.base.message import MessageRepository, MessageModel
from app.repositories.base.role import RoleRepository

from typing import List,Optional

import logging

class MessageService:
    logger = logging.getLogger(__name__)

    def __init__(self, message_repository: MessageRepository,role_repository:RoleRepository) -> None:
        self.message_repository = message_repository
        self.role_repository = role_repository

    def list_messages(self) -> List[MessageModel]:
        try:
            self.logger.info("Reading all messages")
            data = self.message_repository.read_messages_all()
            self.logger.info("Read all messages")
            return data
        except Exception as e:
            self.logger.error("Failed to read all messages: {}".format(e))
            return []
    def list_messages_by_role(self, role: str) -> List[MessageModel]:
        try:
            self.logger.info("Reading all messages by role: {}".format(role))
            messages = self.message_repository.read_messages_by_role(role)
            self.logger.info("Read all messages by role: {}".format(role))
            return messages
        except Exception as e:
            self.logger.error("Failed to read all messages by role: {}".format(e))
            return []
    def read_message(self, message_id: int) -> Optional[MessageModel]:
        try:
            self.logger.info("Reading message: {}".format(message_id))
            message = self.message_repository.read_message_by_id(message_id)
            self.logger.info("Read message: {}".format(message))
            return message
        except Exception as e:
            self.logger.error("Failed to read message: {}".format(e))
            return None
    def create_message(self, message: MessageModel) -> bool:
        try:
            self.logger.info("Creating message: {}".format(message))
            if message.role_name:
                role = self.role_repository.read_role_by_name(message.role_name)
                if role is None:
                    self.logger.error(f"Failed to read role: {role=}")
                    return False
                message.role = role
                isCreated = self.message_repository.create_message(message)
                self.logger.info("Create message: {}".format(isCreated))
                return isCreated
            self.logger.error(f"Failed to create message: {message.role_name=}")
            return False
        except Exception as e:
            self.logger.error("Failed to create message: {}".format(e))
            return False
    def update_message(self, message_id: int, new_message: MessageModel) -> bool:
        try:
            self.logger.info("Updating message: {}".format(new_message.text))
            old_message = self.message_repository.read_message_by_id(message_id)
            if not old_message:
                self.logger.error(f"Failed to update message: {old_message=}")
                return False
            if old_message.role != new_message.role:
                self.logger.error(f"Failed to update message: {(old_message.role != new_message.role)=}")
                return False
            old_message.text = new_message.text
            self.logger.info("Update message: {}".format(new_message.text))
            return self.message_repository.update_message(message_id, old_message)
        except Exception as e:
            self.logger.error("Failed to update message: {}".format(e))
            return False
    def delete_message(self, message_id: int) -> bool:
        try:
            self.logger.info("Deleting message: {}".format(message_id))
            isDelete = self.message_repository.delete_message(message_id=message_id)
            self.logger.info("Delete message: {}".format(isDelete))
            return isDelete
        except Exception as e:
            self.logger.error("Failed to delete message: {}".format(e))
            return False