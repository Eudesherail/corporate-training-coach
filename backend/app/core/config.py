from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Corporate Training Coach"
    api_prefix: str = "/api"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    database_url: str = "sqlite:///./app/data/corporate_training_coach.db"
    openai_api_key: str | None = None
    chat_model: str = "gpt-4o-mini"
    retrieval_mode: str = "keyword"
    cors_origins: list[str] = ["http://localhost:4200"]
    upload_dir: str = "app/data/uploads"
    max_chunk_chars: int = 1400
    chunk_overlap_chars: int = 220
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def upload_path(self) -> Path:
        return Path(__file__).resolve().parents[1] / "data" / "uploads"


@lru_cache
def get_settings() -> Settings:
    return Settings()
