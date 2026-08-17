from app.repositories.base.generic import GenericRepository
from app.models.ai_model import AIModel

class AIModelRepository(GenericRepository[AIModel]):
    def _model_class(self) -> type:
        return AIModel