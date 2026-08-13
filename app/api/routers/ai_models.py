from app.core.config import settings

from app.core.dependencies import get_message_service,MessageService

from fastapi import APIRouter,Depends
from fastapi.responses import RedirectResponse
from openai import OpenAI


client = OpenAI(
  base_url=settings.OPENROUTER_API_BASE_URL,
  api_key=settings.OPENROUTER_API_KEY,
)


router = APIRouter(prefix="/api/v1/ai", tags=["AI Models"])

@router.get("/")
async def root(message: str | None = None,message_service: MessageService = Depends(get_message_service)):

    messages = message_service.list_messages()
    render_messages = []
    for message in messages:
        render_messages.append({"role": ("user" if message.role_name == "Пользователь" else "assistant"), "content":message.text})
    try:
        if message:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=render_messages,
                extra_body={"reasoning": {"enabled": True}}
            )
            return {"message": response.choices[0].message.content}
        else:
            return RedirectResponse(url="/error?code=404", status_code=302)
    except Exception as e:
        return RedirectResponse(url="/error?code=500", status_code=302)


