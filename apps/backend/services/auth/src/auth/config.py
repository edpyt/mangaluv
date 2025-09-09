"""Authentication service config."""

from typing import ClassVar

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseModel):
    """Database connection config."""

    uri: PostgresDsn = PostgresDsn(
        "postgresql+psycopg://user:pass@localhost:5432/auth_db"
    )


class JwtSettings(BaseModel):
    """JWT config."""

    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_expire_minutes: int = 30
    refresh_expire_minutes: int = 30


class Settings(BaseSettings):
    """Main settings class for authentication service."""

    db: DbSettings = Field(default_factory=DbSettings)
    jwt: JwtSettings = Field(default_factory=JwtSettings)

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_nested_delimiter="__"
    )
