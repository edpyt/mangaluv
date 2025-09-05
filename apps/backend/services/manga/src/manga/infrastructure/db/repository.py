# ruff: noqa: D107
"""Manga infrastructure repository module."""

from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from manga.application.dto import MangaDTO
from manga.application.repository import MangaRepository


class MangaRepositoryImpl(MangaRepository):
    """Implementation manga repository interface."""

    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def get_by_id(self, manga_id: int) -> MangaDTO | None:
        raise NotImplementedError

    @override
    async def get_all(self) -> list[MangaDTO]:
        raise NotImplementedError
