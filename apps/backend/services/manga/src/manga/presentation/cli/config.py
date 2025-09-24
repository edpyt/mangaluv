"""Configuration module for manga CLI."""

from typing import ClassVar

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for manga service CLI."""

    db_uri: PostgresDsn = PostgresDsn(
        "postgresql+psycopg://postgre:postgre@localhost:5432/manga_db"
    )

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="MANGA_CLI_", env_nested_delimiter="__"
    )
