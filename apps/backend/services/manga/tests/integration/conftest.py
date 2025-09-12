import os
from collections.abc import AsyncGenerator, Generator
from concurrent.futures import ProcessPoolExecutor
from importlib.resources import files

import pytest
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from manga.infrastructure.db.repository import MangaRepositoryImpl
from manga.presentation.api import start_app
from manga.presentation.api.config import Settings
from manga.presentation.api.di.db import sqla_session_ctx
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from tests.integration.helpers.robyn import check_server_startup


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


@pytest.fixture
def manga_repository(sqla_session: AsyncSession) -> MangaRepositoryImpl:
    return MangaRepositoryImpl(sqla_session)


@pytest.fixture(scope="session")
def start_app_port(db: PostgresContainer) -> Generator[int]:
    os.environ["MANGA_API__db_uri"] = db.get_connection_url()
    os.environ["MANGA_API__test_mode"] = "True"

    host, port = "127.0.0.1", 8080
    with ProcessPoolExecutor() as executor:
        future = executor.submit(start_app, host=host, port=port)
        check_server_startup(future, host, port)
        yield port
        future.cancel()
        for process in executor._processes.values():
            process.kill()


@pytest.fixture
async def client(start_app_port: int) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        base_url=f"http://localhost:{start_app_port}",
    ) as client:
        yield client
