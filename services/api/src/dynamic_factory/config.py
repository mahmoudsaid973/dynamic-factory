"""Application configuration."""

import base64
import hashlib
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[4] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = "postgresql+asyncpg://factory:***@localhost:5432/factory"
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "change-me-in-production"
    encryption_key: str = ""

    def fernet_key(self) -> str:
        """Return a Fernet-compatible key."""
        if self.encryption_key:
            return self.encryption_key
        digest = hashlib.sha256(self.secret_key.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest).decode("ascii")


settings = Settings()
