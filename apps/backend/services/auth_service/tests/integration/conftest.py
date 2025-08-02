from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from dishka import (
    AsyncContainer,
    FromDishka,
    Provider,
    Scope,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.auth_service.db.models import Base
from src.auth_service.main import create_app
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def db() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:16.9-bookworm") as postgres:
        yield postgres


class TestDbProvider(Provider):
    db_uri: str

    def __init__(self, /, db_uri: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_uri = db_uri

    @provide(scope=Scope.APP)
    async def _sqla_async_engine(self) -> AsyncGenerator[AsyncEngine]:
        engine = create_async_engine(self.db_uri)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield engine
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)

    @provide(scope=Scope.APP)
    def _sqla_async_sessionmaker(
        self, engine: FromDishka[AsyncEngine]
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    async def _sqla_async_session(
        self,
        engine: FromDishka[AsyncEngine],
        async_session: FromDishka[async_sessionmaker[AsyncSession]],
    ) -> AsyncGenerator[AsyncSession]:
        async with engine.connect() as conn:
            async with async_session() as session:
                yield session
            await conn.rollback()


@pytest_asyncio.fixture
async def container(db: PostgresContainer) -> AsyncGenerator[AsyncContainer]:
    db_uri = db.get_connection_url().replace(
        "postgresql+psycopg2",
        "postgresql+asyncpg",
    )
    container = make_async_container(TestDbProvider(db_uri))
    yield container
    await container.close()


@pytest.fixture
def app(container: AsyncContainer) -> FastAPI:
    app = create_app()
    setup_dishka(container, app)
    return app


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client
