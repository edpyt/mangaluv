from collections.abc import AsyncGenerator, Generator
from concurrent.futures import ProcessPoolExecutor
from importlib.resources import files
from secrets import token_urlsafe

import pytest
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from manga.infrastructure.db.models import Manga
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
) -> AsyncEngine:
    return create_async_engine(db.get_connection_url())


@pytest.fixture(scope="session", autouse=True)
async def _start_alembic_migrations(
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


@pytest.fixture(scope="session")
def start_app_port(db: PostgresContainer) -> Generator[int]:
    def _init_worker(env_vars: dict[str, str]):
        import os

        os.environ.update(env_vars)

    host, port = "127.0.0.1", 8080
    with ProcessPoolExecutor(
        initializer=_init_worker,
        initargs=(
            {
                "MANGA_API_db_uri": db.get_connection_url(),
                "MANGA_API_test_mode": "True",
            },
        ),
    ) as executor:
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


@pytest.fixture
async def create_random_mangas(
    sqla_sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[list[Manga]]:
    async with sqla_sessionmaker() as session:
        mangas = [Manga(title=token_urlsafe()) for _ in range(10)]
        session.add_all(mangas)
        await session.commit()
        for manga in mangas:
            await session.refresh(manga)
        yield mangas
        await session.reset()
