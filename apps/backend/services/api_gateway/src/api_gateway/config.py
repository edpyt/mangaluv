"""Gateway config code."""

from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Services(BaseModel):
    """Separate services settings."""

    auth_service: HttpUrl = HttpUrl("http://localhost:8001")


class Settings(BaseSettings):
    """API settings."""

    services: Services = Field(default_factory=Services)
    model_config = SettingsConfigDict(env_nested_delimiter="__")


# FIXME: global variable
settings = Settings()
