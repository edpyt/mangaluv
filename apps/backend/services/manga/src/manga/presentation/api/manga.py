"""Manga API routes."""

from uuid import UUID

from robyn import SubRouter
from robyn.types import PathParams

from manga.application.dto import MangaDTO
from manga.domain.errors import MangaNotFoundError
from manga.presentation.api.di import GlobalDependencies
from manga.presentation.api.di.db import manga_service_ctx
from manga.presentation.api.errors.manga import InvalidMangaIdError
from manga.presentation.api.schemas.manga import (
    ErrorGetMangaResponse,
    RetrieveAllMangasResponse,
    SuccessfulGetMangaResponse,
)

router = SubRouter(__file__, prefix="titles")


@router.exception
def _handle_manga_subrouter_errors(  # pyright: ignore[reportUnusedFunction]
    exc: Exception,
) -> tuple[ErrorGetMangaResponse, dict[str, str], int]:
    match exc:
        case InvalidMangaIdError():
            return {"success": False, "error": str(exc)}, {}, 400
        case MangaNotFoundError():
            return {"success": False, "error": str(exc)}, {}, 404
        case _:
            raise exc


@router.get("/")
async def get_all_manga(
    global_dependencies: GlobalDependencies,
) -> RetrieveAllMangasResponse:
    """Retrieve all finded mangas in storage."""
    async with manga_service_ctx(global_dependencies) as manga_service:
        result = await manga_service.get_all_manga()
    return {"titles": result, "total": len(result)}


@router.get("/:manga_id")
async def get_manga(
    path_params: PathParams,
    global_dependencies: GlobalDependencies,
) -> SuccessfulGetMangaResponse:
    """Return manga finded by id."""
    try:
        manga_id = UUID(
            path_params["manga_id"],
            version=4,  # TODO: uuid version in config class
        )
    except ValueError as e:
        raise InvalidMangaIdError() from e

    async with manga_service_ctx(global_dependencies) as manga_service:
        result: MangaDTO = await manga_service.get_manga_by_id(manga_id)

    return {"success": True, "manga": result}
