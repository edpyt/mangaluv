from collections.abc import AsyncGenerator, Generator
from importlib.resources import files

import pytest
from alembic.command import upgrade
from alembic.config import Config
from manga.presentation.api.config import Settings
from manga.presentation.api.di.db import sqla_session_ctx
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def db() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:16.9-alpine") as postgres:
        postgres.driver = "+psycopg"
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
) -> AsyncEngine:
    return create_async_engine(db.get_connection_url())


@pytest.fixture(scope="session", autouse=True)
async def _start_alembic_migrations(  # pyright: ignore[reportUnusedFunction]
    sqla_engine: AsyncEngine,
    alembic_config: Config,
):
    async with sqla_engine.begin() as conn:
        await conn.run_sync(lambda _: upgrade(alembic_config, "head"))


@pytest.fixture(scope="session")
def sqla_sessionmaker(
    sqla_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(sqla_engine)


@pytest.fixture
async def sqla_session(
    sqla_engine: AsyncEngine,
    sqla_sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with sqla_session_ctx(
        {
            "sqla_engine": sqla_engine,
            "sqla_sessionmaker": sqla_sessionmaker,
            "config": Settings(test_mode=True),
        }
    ) as session:
        yield session
