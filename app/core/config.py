from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pathlib import Path

import logging

load_dotenv()

class Settings(BaseSettings):

    DATABASE_URL : str = os.getenv("DATABASE_URL")

    OPENROUTER_API_KEY : str = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_BASE_URL : str = os.getenv("OPENROUTER_API_BASE_URL")

    DEBUG: bool = os.getenv("DEBUG") == "True"

    BASE_DIR:Path = Path(__file__).resolve().parent.parent
    STATIC_DIR:Path = BASE_DIR / "static"
    TEMPLATES_DIR:Path = BASE_DIR / "templates"

    LOGGING_LEVEL: int = ( logging.DEBUG if DEBUG else logging.INFO )

settings = Settings()

logging.basicConfig(level=settings.LOGGING_LEVEL)
