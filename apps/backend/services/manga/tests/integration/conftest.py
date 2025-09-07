from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from manga.infrastructure.db.models import Base
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
        postgres.driver = "+asyncpg"  # pyright: ignore[reportAttributeAccessIssue]
        yield postgres


@pytest_asyncio.fixture(scope="session")
async def sqla_engine(db: PostgresContainer) -> AsyncEngine:
    engine = create_async_engine(db.get_connection_url())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


@pytest.fixture(scope="session")
def sqla_sessionmaker(
    sqla_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(sqla_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def sqla_session(
    sqla_engine: AsyncEngine,
    sqla_sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with sqla_engine.connect() as conn:
        async with sqla_sessionmaker() as session:
            yield session
        await conn.rollback()
