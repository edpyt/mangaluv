"""Manga service repository interfaces."""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from manga.application.dto import MangaDTO


class Repository(Protocol):
    """Base repository protocol."""


class MangaRepository(Repository, Protocol):
    """Manga repository interface."""

    @abstractmethod
    async def create(self, manga_dto: MangaDTO) -> MangaDTO:
        """Create manga in persistence by provided DTO."""

    @abstractmethod
    async def get_by_id(self, manga_id: UUID) -> MangaDTO | None:
        """Search manga by provided id."""

    @abstractmethod
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MangaDTO]:
        """Return all mangas."""
