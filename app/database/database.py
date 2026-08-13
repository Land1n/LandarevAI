from app.core.config import settings

from sqlmodel import create_engine,Session,SQLModel,select

from app.models.role import RoleModel

engine = create_engine(settings.DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for role_name in ["Пользователь", "LandarevAI"]:
            existing = session.exec(
                select(RoleModel).where(RoleModel.name == role_name)
            ).first()
            if not existing:
                session.add(RoleModel(name=role_name))
        session.commit()