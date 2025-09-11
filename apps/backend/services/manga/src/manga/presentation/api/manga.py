"""Manga API routes."""

from robyn import SubRouter
from robyn.types import PathParams

router = SubRouter(__file__)


@router.get("/:manga_id")
async def get_manga(path_params: PathParams) -> str:
    """Return manga finded by id."""
    manga_id = path_params["manga_id"]
    return f"hello,world. {manga_id=}"
