from app.core.config import settings
from app.core.dependencies import (
    get_message_service, MessageService,
    get_ai_model_service, AIModelService,
    get_chat_service, ChatService
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter(prefix="/api/v1/ai", tags=["AI Models"])


class AnswerManager:
    fake_messages = ["Это не настоящее сообщение", "Fake message", "Неправда", "Ложь"]

    def __init__(self, model_url: str = "openrouter/free"):
        self.model_url = model_url
        self.api_agent = OpenAI(
            base_url=settings.OPENROUTER_API_BASE_URL,
            api_key=settings.OPENROUTER_API_KEY,
        )

    def get_answer(self, messages: List[dict]) -> dict:
        if settings.DEBUG:
            return {"message": random.choice(self.fake_messages)}
        else:
            response = self.api_agent.chat.completions.create(
                model=self.model_url,
                messages=messages,
                extra_body={"reasoning": {"enabled": True}}
            )
            return {"message": response.choices[0].message.content}


# Новый эндпоинт: отправка сообщения в чат с использованием сохранённой модели
class ChatMessageRequest(BaseModel):
    message: str


@router.post("/chat/{chat_id}/message")
async def send_message_to_chat(
        chat_id: int,
        req: ChatMessageRequest,
        chat_service: ChatService = Depends(get_chat_service),
        message_service: MessageService = Depends(get_message_service)
):
    chat = chat_service.read_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    model_url = chat.model.url if chat.model else "openrouter/free"
    messages = chat.messages
    render_messages = []
    for msg in messages:
        render_messages.append({
            "role": "user" if msg.role_name == "Пользователь" else "assistant",
            "content": msg.text
        })

    render_messages.append({"role": "user", "content": req.message})

    # Получаем ответ AI
    manager = AnswerManager(model_url=model_url)
    try:
        response = manager.get_answer(render_messages)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")


# Генерация названия — также используем модель чата
class TitleRequest(BaseModel):
    messages: List[dict]
    chat_id: int  # добавим chat_id, чтобы взять модель


class TitleResponse(BaseModel):
    title: str


@router.post("/generate-title", response_model=TitleResponse)
async def generate_title(
        req: TitleRequest,
        chat_service: ChatService = Depends(get_chat_service)
):
    chat = chat_service.read_chat_by_id(req.chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    model_url = chat.model.url if chat.model else "openrouter/free"

    manager = AnswerManager(model_url=model_url)
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
    if len(title) > 30:
        title = title[:30] + "..."
    return TitleResponse(title=title)


# Список моделей (оставлен без изменений)
@router.get("/ai-model")
async def list_ai_model(ai_model_service: AIModelService = Depends(get_ai_model_service)):
    return ai_model_service.list_models()