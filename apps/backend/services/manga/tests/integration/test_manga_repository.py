from manga.application.dto import MangaDTO
from manga.infrastructure.db.models import Manga
from manga.infrastructure.db.repository import MangaRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_by_id(sqla_session: AsyncSession):
    manga_repository = MangaRepositoryImpl(sqla_session)

    result = await manga_repository.get_by_id(1)

    assert result is None

    manga = Manga()
    sqla_session.add(manga)

    result = await manga_repository.get_by_id(1)

    assert isinstance(result, MangaDTO)
    assert result.id == 1
