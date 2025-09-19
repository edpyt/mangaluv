"""Various converter functions for manga model."""

from adaptix.conversion import get_converter

from manga.application.dto import MangaDTO
from manga.infrastructure.db.models import Manga

convert_manga_to_dto = get_converter(Manga, MangaDTO)
convert_dto_to_manga = get_converter(MangaDTO, Manga)
