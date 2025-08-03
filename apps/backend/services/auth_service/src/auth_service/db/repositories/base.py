"""Base repository module."""

from typing import Protocol

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class Repository(Protocol):
    """Repository interface."""


class SQLARepository(Repository):
    """SQLAlchemy repository."""

    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        """
        Init method for SQLAlchemy repository.

        :param session: SQLAlchemy session.
        """
        self.session = session

    async def save(self, instance: object) -> SQLAlchemyError | None:
        """
        Save provided SQLAlchemy model to database.

        :param instance: model instance
        """
        try:
            self.session.add(instance)
            await self.session.commit()
            return await self.session.refresh(instance)
        except SQLAlchemyError as ex:
            return ex
