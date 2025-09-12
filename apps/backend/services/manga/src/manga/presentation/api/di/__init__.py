from typing import TypedDict

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from manga.presentation.api.config import Settings


class GlobalDependencies(TypedDict):
    """Robyn global dependencies."""

    config: Settings
    sqla_engine: AsyncEngine
    sqla_sessionmaker: async_sessionmaker[AsyncSession]
