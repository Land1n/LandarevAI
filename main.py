from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

@app.get("/api")
async def root(message: str | None = None):
    try:
        if message:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=[{"role": "user","content": message }],
                extra_body={"reasoning": {"enabled": True}}
            )
            return {"message": response.choices[0].message.content}
        else:
            return {"message": "No query provided"}
    except Exception as e:
        return {"message": str(e)}


from fastapi import  Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime
import markdown
import bleach

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

messages = [
]

def render_markdown(text):
    # Преобразуем Markdown в HTML
    html = markdown.markdown(text, extensions=['extra', 'codehilite'])
    # Очищаем HTML для безопасности
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


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    # Преобразуем сообщения в HTML для отображения
    rendered_messages = []
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

    return templates.TemplateResponse(name="chat.html",request={
        "request": request,
        "messages": rendered_messages
    })

@app.post("/send")
async def send_message(username: str = Form(...), text: str = Form(...)):
    if text.strip():
        messages.append({
            "username": username or "Аноним",
            "text": text.strip(),
            "time": datetime.now().strftime("%H:%M")
        })
    return {"status": "ok"}

@app.get("/messages")
async def get_messages():
    return messages

