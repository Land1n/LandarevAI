from app.repositories.base.generic import abstractmethod, ABC, GenericRepository

from app.models.message import MessageModel

from app.core.logger.schemas.answer import Answer


class MessageRepository(GenericRepository[MessageModel]):
    @abstractmethod
    def read_by_role(self,role_name:str) -> Answer[MessageModel]:
        pass

    def _model_class(self) -> type:
        return MessageModel