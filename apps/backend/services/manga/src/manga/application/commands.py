"""Application layer commands."""

from typing import TypedDict


class CreateMangaCommand(TypedDict):
    """Dictionary for create manga."""

    title: str
    description: str
