"""Manga API routes."""

from robyn import SubRouter
from robyn.types import PathParams

from manga.application.dto import MangaDTO
from manga.presentation.api.di import GlobalDependencies
from manga.presentation.api.di.db import manga_service_ctx

router = SubRouter(__file__)


@router.get("/:manga_id")
async def get_manga(
    path_params: PathParams,
    global_dependencies: GlobalDependencies,
) -> MangaDTO | tuple[dict[str, str], dict[str, str], int]:
    """Return manga finded by id."""
    manga_id = path_params["manga_id"]
    if not manga_id.isdigit():
        return {"error": "Provided bad manga id"}, {}, 400

    async with manga_service_ctx(global_dependencies) as manga_service:
        return await manga_service.get_manga_by_id(int(manga_id))
