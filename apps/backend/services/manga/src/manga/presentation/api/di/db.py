"""Database dependency injection utilities."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from manga.presentation.api.di import GlobalDependencies


@asynccontextmanager
async def sqla_session_ctx(
    global_dependencies: GlobalDependencies,
) -> AsyncGenerator[AsyncSession]:
    """Return SQLAlchemy async session from `Robyn` DI."""
    sqla_sessionmaker = global_dependencies["sqla_sessionmaker"]
    match global_dependencies["config"].test_mode:
        case True:
            async with global_dependencies["sqla_engine"].begin() as con:
                async with sqla_sessionmaker(
                    bind=con,
                    join_transaction_mode="create_savepoint",
                ) as session:
                    yield session
                await con.rollback()
        case False:
            async with sqla_sessionmaker() as session:
                yield session
