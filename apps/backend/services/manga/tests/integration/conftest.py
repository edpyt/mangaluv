from collections.abc import AsyncGenerator, Generator
from importlib.resources import files

import pytest
from alembic.command import upgrade
from alembic.config import Config
from manga.infrastructure.db.repository import MangaRepositoryImpl
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def db() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:16.9-alpine") as postgres:
        postgres.driver = "+psycopg"  # pyright: ignore[reportAttributeAccessIssue]
        yield postgres


@pytest.fixture(scope="session")
def alembic_config(db: PostgresContainer) -> Config:
    config = Config(
        toml_file=str(files("manga").joinpath("../../pyproject.toml"))
    )
    config.set_main_option("sqlalchemy.url", db.get_connection_url())
    return config


@pytest.fixture(scope="session")
async def sqla_engine(
    db: PostgresContainer,
    alembic_config: Config,
) -> AsyncEngine:
    engine = create_async_engine(db.get_connection_url())

    async with engine.begin() as conn:
        await conn.run_sync(lambda _: upgrade(alembic_config, "head"))
    return engine


@pytest.fixture
async def sqla_session(
    sqla_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession]:
    async with sqla_engine.begin() as conn:
        yield AsyncSession(
            bind=conn,
            join_transaction_mode="create_savepoint",
        )
        await conn.rollback()


@pytest.fixture
def manga_repository(sqla_session: AsyncSession) -> MangaRepositoryImpl:
    return MangaRepositoryImpl(sqla_session)
