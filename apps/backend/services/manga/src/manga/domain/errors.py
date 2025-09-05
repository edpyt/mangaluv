"""Domain errors."""


class DomainException(Exception):
    """Base domain layer exception."""


class MangaNotFoundError(DomainException):
    """Manga not found."""
