from app.core.config import settings
from app.core.dependencies import get_message_service,MessageService
from app.core.dependencies import get_role_service,RoleService

from app.database.database import create_db_and_tables

from fastapi import APIRouter, Request, Depends

from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import markdown
import bleach


router = APIRouter(prefix="/chat", tags=["AI Chat"])

def render_markdown(text):
    html = markdown.markdown(text, extensions=['extra', 'codehilite'])
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 's', 'code', 'pre',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote',
        'a', 'img', 'span', 'div', 'hr'
    ]
    allowed_attrs = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title'],
        'span': ['class'],
        'code': ['class'],
        'pre': ['class']
    }
    return bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)


@router.get("/", response_class=HTMLResponse)
async def chat_page(
        request: Request,
        message_service: MessageService = Depends(get_message_service),
        role_service:RoleService = Depends(get_role_service)
):
    try:
        create_db_and_tables()
        templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
        rendered_messages = []
        messages = message_service.list_messages()

        for msg in messages:
            if msg.get('is_markdown', False):
                rendered_text = render_markdown(msg['text'])
            else:
                rendered_text = msg['text']
            rendered_messages.append({
                'username': msg['username'],
                'text': rendered_text,
                'time': msg['time'],
                'is_markdown': msg.get('is_markdown', False)
            })

        return templates.TemplateResponse(
            name="chat.html",
            request=request,
            context={
                "messages": rendered_messages
            }
        )
    except FileNotFoundError as e:
        return RedirectResponse(url="/error?code=404", status_code=302)
    except ValueError as e:
        return RedirectResponse(url="/error?code=400", status_code=302)
    except PermissionError as e:
        return RedirectResponse(url="/error?code=403", status_code=302)
    except Exception as e:
        return RedirectResponse(url="/error?code=500", status_code=302)
