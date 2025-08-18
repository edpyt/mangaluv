from collections.abc import AsyncGenerator

import pytest_asyncio
from alembic.command import upgrade
from alembic.config import Config
from auth_service.di import ConfigProvider, RepositoriesProvider
from auth_service.main import create_app
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
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator[PostgresContainer]:
    with PostgresContainer("postgres:16.9-bookworm") as postgres:
        yield postgres


@pytest_asyncio.fixture(loop_scope="session")
async def container(db: PostgresContainer) -> AsyncGenerator[AsyncContainer]:
    db.driver = "+asyncpg"  # pyright: ignore[reportAttributeAccessIssue]
    db_uri = db.get_connection_url()
    container = make_async_container(
        ConfigProvider(),  # FIXME: not sure about this
        TestDbProvider(db_uri),
        RepositoriesProvider(),
    )
    yield container
    await container.close()


@pytest_asyncio.fixture(loop_scope="session")
async def app(container: AsyncContainer) -> FastAPI:
    app = create_app()
    setup_dishka(container, app)
    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


class TestDbProvider(Provider):
    db_uri: str

    def __init__(self, /, db_uri: str):
        super().__init__()
        self.db_uri = db_uri

    @provide(scope=Scope.APP)
    async def _alembic_config(self) -> Config:
        config = Config()
        config.set_main_option(
            "script_location", "src/auth_service/db/migrations"
        )
        config.set_main_option("sqlalchemy.url", self.db_uri)
        return config

    @provide(scope=Scope.APP)
    async def _sqla_async_engine(
        self, alembic_config: FromDishka[Config]
    ) -> AsyncGenerator[AsyncEngine]:
        engine = create_async_engine(self.db_uri)
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: upgrade(alembic_config, "head"))
        yield engine

    @provide(scope=Scope.APP)
    def _sqla_async_sessionmaker(
        self, engine: FromDishka[AsyncEngine]
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

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
