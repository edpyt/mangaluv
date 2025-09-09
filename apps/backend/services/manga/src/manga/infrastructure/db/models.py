"""Manga database ORM models."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base ORM model."""


class Manga(Base):
    """Manga ORM model."""

    __tablename__: str = "manga"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column()

    chapters: Mapped[list["Chapter"]] = relationship(back_populates="manga")


class Chapter(Base):
    """Manga chapter model."""

    __tablename__: str = "chapters"
    id: Mapped[int] = mapped_column(primary_key=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))
    manga: Mapped[Manga] = relationship(back_populates="chapters")
