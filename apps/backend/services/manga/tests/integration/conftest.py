from collections.abc import AsyncGenerator, Generator

import pytest
from manga.infrastructure.db.models import Base
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
async def sqla_engine(db: PostgresContainer) -> AsyncEngine:
    engine = create_async_engine(db.get_connection_url())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
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
