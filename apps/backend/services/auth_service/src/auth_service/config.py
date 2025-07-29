"""Authentication service config."""

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseModel):
    """Database connection config."""

    uri: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://user:pass@auth_db:5432/auth_db"
    )


class JwtSettings(BaseModel):
    """JWT config."""

    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    expire_minutes: int = 30


class Settings(BaseSettings):
    """Main settings class for authentication service."""

    db: DbSettings = Field(default_factory=DbSettings)
    jwt: JwtSettings = Field(default_factory=JwtSettings)

    model_config = SettingsConfigDict(env_nested_delimiter="__")
