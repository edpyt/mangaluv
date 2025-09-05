from dataclasses import dataclass  # noqa: D100


@dataclass(frozen=True, kw_only=True)
class MangaDTO:
    """Manga data-transfer object."""

    id: int
