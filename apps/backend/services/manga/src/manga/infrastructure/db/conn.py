# ruff: noqa: D103
"""Database connection logic."""

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


def sqla_session_maker(
    sqla_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(sqla_engine, expire_on_commit=False)


async def sqla_session(
    sqla_session_maker: async_sessionmaker[AsyncSession],
) -> AsyncSession:
    async with sqla_session_maker() as session:
        return session
