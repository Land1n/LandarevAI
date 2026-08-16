from app.repositories.base.role import RoleRepository,RoleModel

from app.core.logger.logger import convert_result, logger
from app.core.logger.schemas.answer import Answer
from app.repositories.sql_model.generic import SQLModelGenericRepository

from sqlmodel import Session,select

from typing import Optional


class SqlModelRoleRepository(SQLModelGenericRepository[RoleModel],RoleRepository):

    def __init__(self, session:Session ):
        super().__init__(session)

    @convert_result
    @logger("Repository")
    def read_by_name(self, name:str) -> Answer[RoleModel]:
        statement = select(RoleModel).where(RoleModel.name == name)
        entity = self.session.exec(statement).first()
        return Answer[RoleModel](result=entity, description=f"{entity=}")

