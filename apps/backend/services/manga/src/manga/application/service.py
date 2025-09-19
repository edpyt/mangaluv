"""Manga application-layer service."""

from dataclasses import dataclass

from manga.application.commands import CreateMangaCommand
from manga.application.dto import MangaDTO
from manga.application.repository import MangaRepository
from manga.domain.entities import Manga
from manga.domain.errors import MangaNotFoundError


@dataclass(frozen=True, slots=True)
class MangaService:  # noqa: D101
    manga_repo: MangaRepository

    async def get_manga_by_id(self, manga_id: int) -> MangaDTO:
        """
        Return finded manga by provided id.

        :param manga_id: Manga ID in persistence storage
        :return: Manga data-transfer object
        """
        if manga := await self.manga_repo.get_by_id(manga_id):
            return manga
        raise MangaNotFoundError(f"Manga with id {manga_id} not found")

    async def get_all_manga(self) -> list[MangaDTO]:
        """Return all mangas in persistence storage."""
        return await self.manga_repo.get_all()

    async def create_manga(self, manga_create: CreateMangaCommand) -> MangaDTO:
        """
        Create manga with domain validation.

        :param manga_create: Create manga command
        :return: Manga data-transfer object
        """
        entity = Manga(**manga_create)
        manga_dto = MangaDTO.from_domain_entity(entity)
        return await self.manga_repo.create(manga_dto)
