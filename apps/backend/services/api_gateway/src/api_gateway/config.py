"""Gateway config code."""

from functools import lru_cache
from typing import ClassVar

from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Services(BaseModel):
    """Separate services settings."""

    auth_service: HttpUrl = HttpUrl("http://auth_service:8001")


class Settings(BaseSettings):
    """API settings."""

    services: Services = Field(default_factory=Services)
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_nested_delimiter="__"
    )


@lru_cache
def get_config() -> Settings:
    """Dependency get settings function."""
    return Settings()
