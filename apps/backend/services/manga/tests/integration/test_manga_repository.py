from secrets import token_urlsafe

import pytest
from manga.application.dto import MangaDTO
from manga.infrastructure.db.models import Manga
from manga.infrastructure.db.repository import MangaRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def manga_repository(sqla_session: AsyncSession) -> MangaRepositoryImpl:
    return MangaRepositoryImpl(sqla_session)


async def test_get_by_id(manga_repository: MangaRepositoryImpl):
    result = await manga_repository.get_by_id(1)

    assert result is None

    await manga_repository.create(Manga(title=token_urlsafe()))

    result = await manga_repository.get_by_id(1)

    assert isinstance(result, MangaDTO)
    assert result.id == 1


@pytest.mark.usefixtures("create_random_mangas")
async def test_get_all(manga_repository: MangaRepositoryImpl):
    result = await manga_repository.get_all()

    assert len(result) == 10
