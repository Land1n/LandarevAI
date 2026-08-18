from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional

from app.core.config import settings
from app.core.dependencies import (
    get_chat_service, get_message_service,
    ChatService, MessageService,
)
from app.schemas.chat import ChatShema, ChatResponse, ChatCreateResponse
from app.schemas.message import MessageShema
from app.models.chat import ChatModel
from app.models.message import MessageModel
from app.database.database import create_db_and_tables
import markdown
import bleach

router = APIRouter(prefix="/chat", tags=["Chat"])

def render_markdown(text: str) -> str:
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
    chat_id: Optional[int] = Query(None, description="ID чата для отображения"),
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        create_db_and_tables()
        templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

        all_chats = chat_service.list_chats()
        current_chat = None
        if chat_id is not None:
            current_chat = chat_service.read_chat_by_id(chat_id)
        if current_chat is None and all_chats:
            current_chat = max(all_chats, key=lambda c: c.id)
        if current_chat is None:
            new_chat = ChatModel(name="Новый чат")
            created = chat_service.create_chat(new_chat)
            if not created:
                return RedirectResponse(url="/error?code=500", status_code=500)
            current_chat = chat_service.read_chat_by_id(new_chat.id)
            all_chats = chat_service.list_chats()

        messages = current_chat.messages if current_chat else []
        rendered_messages = []
        for msg in messages:
            rendered_messages.append({
                'username': msg.role_name,
                'text': render_markdown(msg.text),
                'time': msg.created_at_time.strftime("%H:%M"),
                'is_markdown': True
            })

        # 4. Передаём в шаблон
        return templates.TemplateResponse(
            name="chat.html",
            request=request,
            context={
                "messages": rendered_messages,
                "chats": all_chats,
                "current_chat_model_url":current_chat.model.url if current_chat and current_chat.model else "openrouter/free",
                "current_chat_id": current_chat.id if current_chat else None,
                "current_chat_name": current_chat.name if current_chat else ""
            }
        )
    except:
        return RedirectResponse(url="/error?code=500", status_code=302)

# ---- API для управления чатами ----

@router.get("/api/", response_model=List[ChatShema])
async def list_chats(chat_service: ChatService = Depends(get_chat_service)):
    return chat_service.list_chats()
@router.post("/api/", response_model=ChatCreateResponse)
async def create_chat(
    chat_data: Optional[ChatShema] = None,
    chat_service: ChatService = Depends(get_chat_service)
):
    name = chat_data.name if chat_data and chat_data.name else "Новый чат"
    new_chat = ChatModel(name=name)
    success = chat_service.create_chat(new_chat)
    if not success:
        raise HTTPException(status_code=500, detail="Ошибка создания чата")
    created = chat_service.read_chat_by_id(new_chat.id)
    if not created:
        raise HTTPException(status_code=500, detail="Чат не найден после создания")
    return created

@router.delete("/api/")
async def delete_all_chats(chat_service: ChatService = Depends(get_chat_service)):
    success = chat_service.delete_all_chats()
    if not success:
        raise HTTPException(status_code=500, detail="Ошибка удаления чатов")
    return {"ok": True}

@router.get("/api/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    chat_service: ChatService = Depends(get_chat_service)
):
    chat = chat_service.read_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=500, detail="get_chat")
    return chat


@router.put("/api/{chat_id}")
async def update_chat(
        chat_id: int,
        chat_data: ChatShema,
        chat_service: ChatService = Depends(get_chat_service)
):
    """Обновить имя и модель чата."""
    existing = chat_service.read_chat_by_id(chat_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Чат не найден")

    # Обновляем поля
    existing.name = chat_data.name
    if chat_data.model_id is not None:
        existing.model_id = chat_data.model_id

    success = chat_service.update_chat(chat_id, existing)
    if not success:
        raise HTTPException(status_code=500, detail="Ошибка обновления чата")
    return {"ok": True}

@router.delete("/api/{chat_id}")
async def delete_chat(
    chat_id: int,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Удалить чат по ID."""
    success = chat_service.delete_chat(chat_id)
    if not success:
        raise HTTPException(status_code=500, detail="delete_chat")
    return {"ok": True}

@router.post("/api/{chat_id}/message")
async def add_message_to_chat(
    chat_id: int,
    message: MessageShema,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Добавить сообщение в чат."""
    # Создаём модель сообщения
    msg_model = MessageModel(text=message.text, role_name=message.role_name)
    success = chat_service.add_message_to_chat(chat_id, msg_model)
    if not success:
        raise HTTPException(status_code=500, detail="add_message_to_chat")
    return {"ok": True}