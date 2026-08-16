from app.repositories.base.generic import GenericRepository,ABC

from app.models.chat import ChatModel

from typing import List,Optional

class ChatRepository(GenericRepository[ChatModel]):
    def _model_class(self) -> type:
        return ChatModel