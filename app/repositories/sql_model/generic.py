from app.repositories.base.generic import GenericRepository,T

from app.core.logger.schemas.answer import Answer
from app.core.logger.logger import logger,convert_result

from sqlmodel import Session,select
from abc import ABC

import logging

class SQLModelGenericRepository(GenericRepository[T],ABC):

    def __init__(self, session: Session):
        self.session = session

    @convert_result
    @logger("Repository")
    def read_all(self) -> Answer[T]:
        try:
            data = list(self.session.exec(select(self._model_class())).all())
            return Answer[T](result=data)
        except Exception as e:
            return Answer[T](result=[], level=logging.ERROR, description=str(e))

    @convert_result
    @logger("Repository")
    def create(self, entity: T) -> Answer[T]:
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return Answer[T](result=True)
        except Exception as e:
            return Answer[T](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("Repository")
    def read_by_id(self, id: int) -> Answer[T]:
        try:
            statement = select(self._model_class()).where(self._model_class().id == id)
            entity = self.session.exec(statement).first()
            return Answer[T](result=entity, description=f"{entity=}")
        except Exception as e:
            return Answer[T](result=None, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("Repository")
    def update(self, id: int, entity: T) -> Answer[T]:
        try:
            old_entity = self.read_by_id(id)
            if old_entity:
                old_entity = entity
                self.session.add(old_entity)
                self.session.commit()
                self.session.refresh(old_entity)
                return Answer[T](result=True)
            return Answer[T](result=False, level=logging.WARNING, description=f"{old_entity=}")
        except Exception as e:
            return Answer[T](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("Repository")
    def delete(self, id: int) -> Answer[T]:
        try:
            entity = self.read_by_id(id)
            if entity:
                self.session.delete(entity)
                self.session.commit()
                return Answer[T](result=True)
            return Answer[T](result=False, level=logging.WARNING, description=f"{entity=}")
        except Exception as e:
            return Answer[T](result=False, level=logging.ERROR, description=str(e))