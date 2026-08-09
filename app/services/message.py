from app.repositories.base.message import MessageRepository, MessageModel

from typing import List,Optional

class MessageService:
    def __init__(self, message_repository: MessageRepository) -> None:
        self.repository = message_repository

    def list_messages(self) -> List[MessageModel]:
        try:
            return self.repository.read_messages_all()
        except:
            return []
    def list_messages_by_role(self, role: str) -> List[MessageModel]:
        try:
            return self.repository.read_messages_by_role(role)
        except:
            return []
    def read_message(self, message_id: int) -> Optional[MessageModel]:
        try:
            return self.repository.read_message_by_id(message_id)
        except:
            return None
    def create_message(self, message: MessageModel) -> bool:
        try:
            return self.repository.create_message(message)
        except:
            return False
    def update_message(self, message_id: int, message: MessageModel) -> bool:
        try:
            return self.repository.update_message(message_id=message_id, message=message)
        except:
            return False
    def delete_message(self, message_id: int) -> bool:
        try:
            return self.repository.delete_message(message_id=message_id)
        except:
            return False