from app.repositories.base.ai_model import AIModelRepository, AIModel
from app.repositories.sql_model.generic import SQLModelGenericRepository
from sqlmodel import Session

class SqlModelAIModelRepository(SQLModelGenericRepository[AIModel], AIModelRepository):
    def __init__(self, session: Session):
        super().__init__(session)