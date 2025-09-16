"""Manga API routes."""

from dataclasses import asdict

from robyn import Response, SubRouter
from robyn.types import PathParams

from manga.application.dto import MangaDTO
from manga.domain.errors import MangaNotFoundError
from manga.presentation.api.di import GlobalDependencies
from manga.presentation.api.di.db import manga_service_ctx

router = SubRouter(__file__, prefix="title")


@router.exception
def _handle_manga_subrouter_errors(exc: Exception) -> Response:  # pyright: ignore[reportUnusedFunction]
    match exc:
        case MangaNotFoundError():
            return Response(
                status_code=404,
                description=str(exc),
                headers={},
            )
        case _:
            raise exc


@router.get("/:manga_id")
async def get_manga(
    path_params: PathParams,
    global_dependencies: GlobalDependencies,
) -> dict[str, int] | Response:
    """Return manga finded by id."""
    manga_id = path_params["manga_id"]
    if not manga_id.isdigit():
        return Response(
            status_code=400,
            description="Provided bad manga id",
            headers={},
        )

    async with manga_service_ctx(global_dependencies) as manga_service:
        result: MangaDTO = await manga_service.get_manga_by_id(int(manga_id))

    return asdict(result)
