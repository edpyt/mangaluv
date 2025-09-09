# ruff: noqa: D107
"""Manga infrastructure repository module."""

from dataclasses import dataclass
from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from manga.application.dto import MangaDTO
from manga.application.repository import MangaRepository
from manga.infrastructure.converters.manga import convert_manga_to_dto
from manga.infrastructure.db.models import Manga


@dataclass
class MangaRepositoryImpl(MangaRepository):
    """Implementation manga repository interface."""

    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def get_by_id(self, manga_id: int) -> MangaDTO | None:
        stmt = select(Manga).where(Manga.id == manga_id)
        result = await self._session.execute(stmt)
        if manga := result.scalar_one_or_none():
            return convert_manga_to_dto(manga)
        return None

    @override
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MangaDTO]:
        stmt = select(Manga).order_by(Manga.id).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return [convert_manga_to_dto(manga) for manga in result.scalars()]
