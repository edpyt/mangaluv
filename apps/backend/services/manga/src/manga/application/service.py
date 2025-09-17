"""Manga application-layer service."""

from manga.application.dto import MangaDTO
from manga.application.repository import MangaRepository
from manga.domain.errors import MangaNotFoundError


class MangaService:  # noqa: D101
    manga_repo: MangaRepository

    def __init__(self, manga_repo: MangaRepository) -> None:  # noqa: D107
        self.manga_repo = manga_repo

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
