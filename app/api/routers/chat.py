from app.core.config import settings

from app.core.dependencies import get_message_service,MessageService

from app.schemas.message import MessageShema
from app.models.message import MessageModel

from app.database.database import create_db_and_tables

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse,RedirectResponse,Response
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
def chat_page(
        request: Request,
        message_service: MessageService = Depends(get_message_service)
):
    try:
        create_db_and_tables()
        templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
        rendered_messages = []
        messages = message_service.list_messages()

        for msg in messages:
            rendered_messages.append({
                'username': msg.role_name,
                'text':  render_markdown(msg.text),
                'time': (msg.created_at_time.strftime("%H:%M")),
                'is_markdown': True
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

@router.post("/")
def send_message(
        message:MessageShema,
        message_service: MessageService = Depends(get_message_service)
):
    create_db_and_tables()

    return {"result": message_service.create_message(MessageModel(**message.model_dump()))}


@router.delete("/")
def delete_all_message(message_service: MessageService = Depends(get_message_service)
):
    create_db_and_tables()

    if all(message_service.delete_message(msg.id) for msg in message_service.list_messages()):
        return Response(status_code=200)
    return RedirectResponse(url="/error?code=500", status_code=302)