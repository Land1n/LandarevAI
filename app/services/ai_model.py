# app/services/ai_model.py
from typing import List, Optional
import logging
from app.repositories.base.ai_model import AIModelRepository, AIModel
from app.core.logger.logger import convert_result, logger
from app.core.logger.schemas.answer import Answer

class AIModelService:
    def __init__(self, repository: AIModelRepository):
        self.repository = repository

    @convert_result
    @logger("AIModelService")
    def list_models(self) -> List[AIModel]:
        try:
            models = self.repository.read_all()
            return Answer[AIModel](result=models, level=logging.INFO)
        except Exception as e:
            return Answer[AIModel](result=[], level=logging.ERROR, description=str(e))

    @convert_result
    @logger("AIModelService")
    def read_model(self, model_id: int) -> Optional[AIModel]:
        try:
            model = self.repository.read_by_id(model_id)
            if model:
                return Answer[AIModel](result=model, level=logging.INFO)
            return Answer[AIModel](
                result=None,
                level=logging.WARNING,
                description=f"Model with id={model_id} not found"
            )
        except Exception as e:
            return Answer[AIModel](result=None, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("AIModelService")
    def create_model(self, model: AIModel) -> bool:
        try:
            is_created = self.repository.create(model)
            return Answer[AIModel](result=is_created, level=logging.INFO)
        except Exception as e:
            return Answer[AIModel](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("AIModelService")
    def update_model(self, model_id: int, model: AIModel) -> bool:
        try:
            old = self.repository.read_by_id(model_id)
            if old is None:
                return Answer[AIModel](
                    result=False,
                    level=logging.ERROR,
                    description=f"Model with id={model_id} not found"
                )
            is_updated = self.repository.update(model_id, model)
            if not is_updated:
                return Answer[AIModel](
                    result=False,
                    level=logging.WARNING,
                    description="Update returned False"
                )
            return Answer[AIModel](result=True, level=logging.INFO)
        except Exception as e:
            return Answer[AIModel](result=False, level=logging.ERROR, description=str(e))

    @convert_result
    @logger("AIModelService")
    def delete_model(self, model_id: int) -> bool:
        try:
            old = self.repository.read_by_id(model_id)
            if old is None:
                return Answer[AIModel](
                    result=False,
                    level=logging.ERROR,
                    description=f"Model with id={model_id} not found"
                )
            is_deleted = self.repository.delete(model_id)
            if not is_deleted:
                return Answer[AIModel](
                    result=False,
                    level=logging.WARNING,
                    description="Delete returned False"
                )
            return Answer[AIModel](result=True, level=logging.INFO)
        except Exception as e:
            return Answer[AIModel](result=False, level=logging.ERROR, description=str(e))