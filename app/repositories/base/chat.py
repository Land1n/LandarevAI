from app.repositories.generic import GenericRepository,ABC

from app.models.chat import ChatModel

from typing import List,Optional

class ChatRepository(GenericRepository[ChatModel]):
    pass
