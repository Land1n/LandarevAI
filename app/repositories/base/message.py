from abc import ABC,abstractmethod
from typing import List

from app.models.message import MessageModel

class MessageRepository(ABC):
    @abstractmethod
    def get_all_messages(self) -> List[MessageModel]:
        pass
    @abstractmethod
    def get_message_by_id(self, message_id: int ) -> MessageModel:
        pass
    @abstractmethod
    def get_message_by_role(self,role_id: int) -> List[MessageModel]:
        pass
    @abstractmethod
    def create_message(self, message_id: int, message: MessageModel) -> bool:
        pass
    @abstractmethod
    def update_message(self, message_id: int, message: MessageModel) -> bool:
        pass
    @abstractmethod
    def delete_message(self, message_id: int) -> bool:
        pass
