# app/repositories/sql_model/chat.py
from app.repositories.base.chat import ChatRepository, ChatModel
from app.repositories.sql_model.generic import SQLModelGenericRepository
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models.message import MessageModel
from app.core.logger.schemas.answer import Answer
from app.core.logger.logger import convert_result, logger
import logging


class SqlModelChatRepository(SQLModelGenericRepository[ChatModel], ChatRepository):

    def __init__(self, session: Session):
        super().__init__(session)

    @convert_result
    @logger("Repository")
    def read_by_id(self, id: int) -> Answer[ChatModel]:
        try:
            statement = (
                select(ChatModel)
                .where(ChatModel.id == id)
                .options(
                    selectinload(ChatModel.messages).selectinload(MessageModel.role),
                    selectinload(ChatModel.model)  # теперь отдельно
                )
            )
            entity:ChatModel = self.session.exec(statement).first()
            return Answer[ChatModel](result=entity, description=f"{entity=}")
        except Exception as e:
            return Answer[ChatModel](result=None, level=logging.ERROR, description=str(e))