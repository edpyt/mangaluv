"""Manga service domain models."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(kw_only=True, frozen=True)
class Manga:
    """Main manga domain model."""

    id: UUID = field(default_factory=uuid4)
    title: str
    description: str
