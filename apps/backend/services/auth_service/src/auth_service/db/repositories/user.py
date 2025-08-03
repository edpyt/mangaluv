"""User repository."""

from sqlalchemy import select

from auth_service.db.models import User
from auth_service.db.repositories.base import SQLARepository


class UserRepository(SQLARepository):
    """User repository class."""

    async def find_by_email(self, email: str) -> User | None:
        """
        Find user by provided email.

        :param email: user email
        :return: finded user SQLAlchemy db model or None
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()
