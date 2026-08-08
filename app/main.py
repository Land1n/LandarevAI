from app.core.config import settings

from app.api.routers.ai_models import ai_models
from app.api.routers.chat import chat

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=str(settings.STATIC_DIR)),
    name="static"
)

app.include_router(ai_models.router)
app.include_router(chat.router)
