from app.repositories.base.message import MessageRepository, MessageModel
from app.repositories.base.role import RoleRepository

from typing import List,Optional


class MessageService:
    def __init__(self, message_repository: MessageRepository,role_repository:RoleRepository) -> None:
        self.message_repository = message_repository
        self.role_repository = role_repository


    def list_messages(self) -> List[MessageModel]:
        try:
            return self.message_repository.read_messages_all()
        except:
            return []
    def list_messages_by_role(self, role: str) -> List[MessageModel]:
        try:
            return self.message_repository.read_messages_by_role(role)
        except:
            return []
    def read_message(self, message_id: int) -> Optional[MessageModel]:
        try:
            return self.message_repository.read_message_by_id(message_id)
        except:
            return None
    def create_message(self, message: MessageModel) -> bool:
        try:
            if message.role_name:
                role = self.role_repository.read_role_by_name(message.role_name)
                if role is None:
                    return False
                message.role = role
                return self.message_repository.create_message(message)
            return False
        except:
            return False
    def update_message(self, message_id: int, message: MessageModel) -> bool:
        try:
            existing = self.message_repository.read_message_by_id(message_id)
            if not existing:
                return False
            existing.text = message.text
            if message.role_name:
                role = self.role_repository.read_role_by_name(message.role_name)
                if role:
                    existing.role_id = role.id
            elif message.role_id is not None:
                existing.role_id = message.role_id
            return self.message_repository.update_message(message_id, existing)
        except Exception as e:
            print(e)
            return False
    def delete_message(self, message_id: int) -> bool:
        try:
            return self.message_repository.delete_message(message_id=message_id)
        except:
            return False