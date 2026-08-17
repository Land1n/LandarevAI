from app.core.config import settings

from sqlmodel import create_engine,Session,SQLModel,select

from app.models.role import RoleModel
from app.models.ai_model import AIModel

engine = create_engine(settings.DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    api_models = [
        "dots-studio/dots-3-note-preview:free",
        "poolside/laguna-s-2.1:free",
        "cohere/north-mini-code:free",
        "google/gemma-4-26b-a4b-it:free",
        "openai/gpt-oss-20b:free",
        "liquid/lfm-2.5-2.6b:free",
        "z-ai/glm-5.2:free",
        "nvidia/nemotron-3-ultra-550b-a55b:free"
    ]

    with Session(engine) as session:
        for role_name in ["Пользователь", "LandarevAI"]:
            existing = session.exec(
                select(RoleModel).where(RoleModel.name == role_name)
            ).first()
            if not existing:
                session.add(RoleModel(name=role_name))

        for url in api_models:
            existing = session.exec(
                select(AIModel).where(AIModel.url == url)
            ).first()
            if not existing:
                session.add(AIModel(url=url))

        session.commit()