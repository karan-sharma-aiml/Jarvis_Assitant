
# Config

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Provider(StrEnum):
    """
    Supported LLM providers.
    """

    OLLAMA = "ollama"
    GEMINI = "gemini"
    GROQ = "groq"
    OPENAI = "openai"


class Settings(BaseSettings):
    """
    Central configuration for JARVIS.
    Values are automatically loaded from the .env file.
    """

    # Application

    APP_NAME: str = "JARVIS"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Logging

    LOG_LEVEL: str = "INFO"

    # Default Provider

    DEFAULT_PROVIDER: Provider = Provider.OLLAMA

    # Ollama

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"

    # Gemini

    GEMINI_API_KEY: str = Field(default="")
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Groq

    GROQ_API_KEY: str = Field(default="")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # OpenAI

    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = "gpt-5"

    # Database

    DATABASE_PATH: str = "data/memory/jarvis.db"

    # Vector Database

    VECTOR_DB_PATH: str = "data/vector_db"

    # Embeddings

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Uploads

    UPLOAD_PATH: str = "data/uploads"

    # SMTP

    SMTP_HOST: str = Field(default="")
    SMTP_PORT: int = Field(default=587)
    SMTP_USERNAME: str = Field(default="")
    SMTP_PASSWORD: SecretStr = Field(default=SecretStr(""))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """

    return Settings()


settings = get_settings()

