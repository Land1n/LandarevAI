from app.core.config import settings

from app.api.routers import ai_models,chat,error

from fastapi.responses import RedirectResponse
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
app.include_router(error.router)

@app.get("/")
def root():
    return RedirectResponse(url="/chat")