# ruff: noqa: D107
"""Manga infrastructure repository module."""

from typing import Any, override
from uuid import UUID

from sqlalchemy import Executable, select
from sqlalchemy.ext.asyncio import AsyncSession

from manga.application.dto import MangaDTO
from manga.application.repository import MangaRepository
from manga.infrastructure.converters.manga import (
    convert_dto_to_manga,
    convert_manga_to_dto,
)
from manga.infrastructure.db.models import Manga


class SQLARepository:
    """SQLAlchemy base repository."""

    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _get_by_stmt(self, stmt: Executable) -> Any | None:  # pyright: ignore[reportExplicitAny]
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def _create(self, instance: Any) -> Any:  # pyright: ignore[reportExplicitAny]
        """Save SQLAlchemy ORM model."""
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance


class MangaRepositoryImpl(MangaRepository, SQLARepository):
    """Implementation manga repository interface."""

    @override
    async def create(self, manga_dto: MangaDTO) -> MangaDTO:
        manga = convert_dto_to_manga(manga_dto)
        manga = await self._create(manga)
        return convert_manga_to_dto(manga)

    @override
    async def get_by_id(self, manga_id: UUID) -> MangaDTO | None:
        stmt = select(Manga).where(Manga.id == manga_id)
        if manga := await self._get_by_stmt(stmt):
            return convert_manga_to_dto(manga)
        return None

    @override
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MangaDTO]:
        stmt = select(Manga).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return [convert_manga_to_dto(manga) for manga in result.scalars()]
