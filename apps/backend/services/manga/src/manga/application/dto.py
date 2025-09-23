"""Manga data-transfer objects."""

from dataclasses import dataclass, field
from typing import Self
from uuid import UUID, uuid4

from manga.domain.entities import Manga


@dataclass(frozen=True, kw_only=True)
class MangaDTO:
    """Manga data-transfer object."""

    id: UUID = field(default_factory=uuid4)
    title: str
    description: str

    @classmethod
    def from_domain_entity(cls, entity: Manga) -> Self:
        """Return DTO from domain entity."""
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
        )
