"""Database dependency injection utilities."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from manga.application.repository import MangaRepository
from manga.application.service import MangaService
from manga.infrastructure.db.repository import MangaRepositoryImpl
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


@asynccontextmanager
async def manga_repository_ctx(
    global_dependencies: GlobalDependencies,
) -> AsyncGenerator[MangaRepository]:
    """Return Manga persistence repository with SQLAlchemy session."""
    async with sqla_session_ctx(global_dependencies) as session:
        yield MangaRepositoryImpl(session)


@asynccontextmanager
async def manga_service_ctx(
    global_dependencies: GlobalDependencies,
) -> AsyncGenerator[MangaService]:
    """Return Manga application-layer service with implemented repository."""
    async with manga_repository_ctx(global_dependencies) as manga_repository:
        yield MangaService(manga_repository)
