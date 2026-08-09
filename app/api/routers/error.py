from starlette.templating import Jinja2Templates

from app.core.config import settings

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/error", tags=["Error"])

@router.get("/", response_class=HTMLResponse)
async def error_page(request: Request, code: str = "500"):
    templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
    return templates.TemplateResponse(
        name="error.html",
        request=request,
        context={
            "code": code
        }
    )