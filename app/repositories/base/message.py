from abc import ABC,abstractmethod
from typing import List,Optional

from app.models.message import MessageModel

class MessageRepository(ABC):
    @abstractmethod
    def read_messages_all(self) -> List[MessageModel]:
        pass
    @abstractmethod
    def read_messages_by_role(self,role_name:str) -> List[MessageModel]:
        pass

    @abstractmethod
    def create_message(self,  message: MessageModel) -> bool:
        pass
    @abstractmethod
    def read_message_by_id(self, message_id: int ) -> Optional[MessageModel]:
        pass
    @abstractmethod
    def update_message(self, message_id: int, message: MessageModel) -> bool:
        pass
    @abstractmethod
    def delete_message(self, message_id: int) -> bool:
        pass
