"""Manga subrouter schemas."""

from robyn.types import JSONResponse

from manga.application.dto import MangaDTO


class RetrieveAllMangasResponse(JSONResponse):
    """Response for get all manga route."""

    titles: list[MangaDTO]
    total: int


class GetMangaResponse(JSONResponse):
    """Response for search manga route."""

    success: bool


class SuccessfulGetMangaResponse(GetMangaResponse):
    """Response if success search manga."""

    manga: MangaDTO


class ErrorGetMangaResponse(GetMangaResponse):
    """Response if error when search manga."""

    error: str
