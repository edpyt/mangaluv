"""Manga service domain models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Manga:
    """Main manga domain model."""

    id: int  # TODO: change to uuid
    title: str
    description: str | None = None


@dataclass(frozen=True)
class Chapter:
    """Manga chapter domain model."""

    id: int
    manga_id: int
    pages: list[str]
