from app.repositories.base.message import MessageRepository,MessageModel

from app.repositories.sql_model.generic import SQLModelGenericRepository

from sqlmodel import Session,select

from app.core.logger.schemas.answer import Answer
from app.core.logger.logger import logger,convert_result

import logging

class SqlModelMessageRepository(SQLModelGenericRepository[MessageModel],MessageRepository):
    def __init__(self, session:Session ):
        super().__init__(session)

    @convert_result
    @logger("Repository")
    def read_by_role(self, role_name: str) -> Answer[MessageModel]:
        return Answer(result=[], level=logging.WARNING, description="This is not work") # TODO: Пока не готово