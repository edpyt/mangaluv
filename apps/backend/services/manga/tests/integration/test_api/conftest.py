from collections.abc import AsyncGenerator, Generator
from concurrent.futures import Future, ProcessPoolExecutor
from secrets import token_urlsafe

import pytest
from httpx import AsyncClient
from manga.infrastructure.db.models import Manga
from manga.presentation.api import start_app
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from testcontainers.postgres import PostgresContainer

from tests.integration.helpers.robyn import (  # pyright: ignore[reportImplicitRelativeImport]
    check_server_startup,
)


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
        future: Future[None] = executor.submit(start_app, host=host, port=port)
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
        mangas = [
            Manga(title=token_urlsafe(), description=token_urlsafe())
            for _ in range(10)
        ]
        session.add_all(mangas)
        await session.commit()
        for manga in mangas:
            await session.refresh(manga)
        yield mangas
        await session.reset()
