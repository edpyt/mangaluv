"""Manga service config."""

from typing import Annotated, ClassVar

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main settings for manga service."""

    db_uri: PostgresDsn = PostgresDsn(
        "postgresql+psycopg://postgre:postgre@localhost:5432/manga_db"
    )
    test_mode: Annotated[
        bool,
        """
    Need for run application in separate procces with
    SQLAlchemy nested transactions.

    Required because Robyn has no support for running in tests.
    https://github.com/sparckles/Robyn/issues/507
    """,
    ] = False

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="MANGA_API_", env_nested_delimiter="__"
    )
