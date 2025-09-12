"""Manga API routes."""

from robyn import SubRouter
from robyn.types import PathParams

router = SubRouter(__file__)


@router.get("/:manga_id")
async def get_manga(
    path_params: PathParams,
) -> str | tuple[dict[str, str], dict[str, str], int]:
    """Return manga finded by id."""
    manga_id = path_params["manga_id"]
    if not manga_id.isdigit():
        return {"error": "Provided bad manga id"}, {}, 400
    return manga_id
