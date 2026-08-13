from app.repositories.generic import abstractmethod,GenericRepository

from app.models.message import MessageModel

from typing import List,Optional

class MessageRepository(GenericRepository[MessageModel]):
    @abstractmethod
    def read_by_role(self,role_name:str) -> List[MessageModel]:
        pass