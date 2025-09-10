"""Manga API routes."""

from robyn import SubRouter

router = SubRouter(__file__, prefix="/")


@router.get("/manga/:manga_id")
async def get_manga(_, path_params):
    """Return manga finded by id."""
    _manga_id = int(path_params.manga_id)
