"""Manga database ORM models."""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase): ...  # noqa: D101


class MangaModel(Base):
    """Manga ORM model."""

    __tablename__: str = "manga"
    id: Mapped[int] = mapped_column(primary_key=True)
    chapters: Mapped[list["ChapterModel"]] = relationship(
        back_populates="manga"
    )


class ChapterModel(Base):
    """Manga chapter model."""

    __tablename__: str = "chapters"
    id: Mapped[int] = mapped_column(primary_key=True)
    manga: Mapped[MangaModel] = relationship(back_populates="chapters")
