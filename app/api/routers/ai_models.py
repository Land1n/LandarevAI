from app.core.config import settings
from app.core.dependencies import get_message_service, MessageService
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter(prefix="/api/v1/ai", tags=["AI Models"])

class AnswerManager:
    fake_messages = ["Это не настоящее сообщение", "Fake message", "Неправда", "Ложь"]

    api_agent = OpenAI(
        base_url=settings.OPENROUTER_API_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
    )

    def get_answer(self, messages: List[dict]) -> dict:
        if settings.DEBUG:
            return {"message": random.choice(self.fake_messages)}
        else:
            response = self.api_agent.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                extra_body={"reasoning": {"enabled": True}}
            )
            return {"message": response.choices[0].message.content}

# Существующий GET-эндпоинт (оставлен без изменений)
@router.get("/")
async def root(
    message: Optional[str] = None,
    message_service: MessageService = Depends(get_message_service)
):
    if not message:
        return RedirectResponse(url="/error?code=404", status_code=302)
    messages = message_service.list_messages()
    render_messages = []
    for msg in messages:
        render_messages.append({
            "role": "user" if msg.role_name == "Пользователь" else "assistant",
            "content": msg.text
        })
    try:
        manager = AnswerManager()
        return manager.get_answer(messages=render_messages)
    except Exception:
        return RedirectResponse(url="/error?code=500", status_code=302)

class TitleRequest(BaseModel):
    messages: List[dict]

class TitleResponse(BaseModel):
    title: str

@router.post("/generate-title", response_model=TitleResponse)
async def generate_title(req: TitleRequest):
    """
    Генерирует короткое название для чата на основе первого сообщения.
    Использует готовый AnswerManager.
    """
    manager = AnswerManager()
    prompt_messages = req.messages + [
        {
            "role": "system",
            "content": (
                "Придумай короткое название (не более 3 слов) для этого чата на русском языке. "
                "Ответь только названием, без кавычек, точек и лишних символов."
            )
        }
    ]
    response = manager.get_answer(prompt_messages)
    title = response.get("message", "Новый чат").strip()
    # Ограничиваем длину и убираем возможные кавычки
    if len(title) > 30:
        title = title[:30] + "..."
    return TitleResponse(title=title)