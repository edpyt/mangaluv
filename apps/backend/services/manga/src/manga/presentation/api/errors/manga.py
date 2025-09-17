"""Manga subrouter errors."""

from typing import override


class InvalidMangaIdError(ValueError):
    """Raises if provided bad id in path params."""

    @override
    def __str__(self) -> str:
        return "Invalid manga ID"
