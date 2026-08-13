from app.core.config import settings

from app.core.dependencies import get_message_service,MessageService

from fastapi import APIRouter,Depends
from fastapi.responses import RedirectResponse

from openai import OpenAI

from typing import List


router = APIRouter(prefix="/api/v1/ai", tags=["AI Models"])

class AnswerManager:

    fake_messages = ["Это не настоящее сообщение", "Fake message", "Неправда","Ложь"]

    api_agent = OpenAI(
        base_url=settings.OPENROUTER_API_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
    )

    def get_answer(self,messages:List[dict]) -> dict:
        if settings.DEBUG:
            import random
            return {"message":random.choice(self.fake_messages)}
        else:
            response = self.api_agent.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                extra_body={"reasoning": {"enabled": True}}
            )
            return {"message":response.choices[0].message.content}

@router.get("/")
async def root(message: str | None = None,message_service: MessageService = Depends(get_message_service)):

    messages = message_service.list_messages()
    render_messages = []
    manager = AnswerManager()

    for message in messages:
        render_messages.append({"role": ("user" if message.role_name == "Пользователь" else "assistant"), "content":message.text})
    try:
        if message:
            return manager.get_answer(messages=render_messages)
        else:
            return RedirectResponse(url="/error?code=404", status_code=302)
    except Exception as e:
        return RedirectResponse(url="/error?code=500", status_code=302)
