from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class Settings(BaseSettings):

    OPENROUTER_API_KEY : str = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_BASE_URL : str = os.getenv("OPENROUTER_API_BASE_URL")

    BASE_DIR:Path = Path(__file__).resolve().parent.parent
    STATIC_DIR:Path = BASE_DIR / "static"
    TEMPLATES_DIR:Path = BASE_DIR / "templates"


settings = Settings()