"""Manga service config."""

from typing import ClassVar

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main settings for manga service."""

    db_uri: PostgresDsn = PostgresDsn(
        "postgresql+psycopg://postgre:postgre@localhost:5432/manga_db"
    )
    test_mode: bool = False

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="MANGA_API_", env_nested_delimiter="__"
    )
