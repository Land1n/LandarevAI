from app.repositories.base.generic import GenericRepository,ABC

from app.models.chat import ChatModel

class ChatRepository(GenericRepository[ChatModel]):
    def _model_class(self) -> type:
        return ChatModel