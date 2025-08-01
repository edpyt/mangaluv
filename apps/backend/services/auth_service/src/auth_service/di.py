"""Setup DI providers."""

from collections.abc import AsyncGenerator

from dishka import (
    AsyncContainer,
    FromDishka,
    Provider,
    Scope,
    make_async_container,
    provide,  # pyright: ignore[reportUnknownVariableType]
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from auth_service.config import Settings


class ConfigProvider(Provider):
    """Config settings provider."""

    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        """Return settings object instance."""
        return Settings()


class DbProvider(Provider):
    """Database DI provider."""

    @provide(scope=Scope.APP)
    def get_sqla_async_engine(
        self, settings: FromDishka[Settings]
    ) -> AsyncEngine:
        """Return SQLAlchemy engine (async)."""
        return create_async_engine(str(settings.db.uri))

    @provide(scope=Scope.APP)
    def get_sqla_async_sessionmaker(
        self, engine: FromDishka[AsyncEngine]
    ) -> async_sessionmaker[AsyncSession]:
        """Return SQLAlchemy asynchronous session maker."""
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_sqla_async_session(
        self,
        async_session: FromDishka[async_sessionmaker[AsyncSession]],
    ) -> AsyncGenerator[AsyncSession]:
        """Return SQLAlchemy asynchronous session."""
        async with async_session() as session:
            yield session


def setup_container() -> AsyncContainer:
    """Return Dishka container."""
    return make_async_container(ConfigProvider(), DbProvider())
