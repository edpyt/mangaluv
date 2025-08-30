"""User repository."""

from sqlalchemy import select

from auth.db.models import User
from auth.db.repositories.base import SQLARepository


class UserRepository(SQLARepository):
    """User repository class."""

    async def find_by_email(self, email: str) -> User | None:
        """
        Find user by provided email.

        :param email: user email
        :return: User instance
        """
        stmt = select(User).where(User.email == email)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def find_by_username(self, username: str) -> User | None:
        """
        Find user by username.

        :param username: username
        :return: User instance
        """
        stmt = select(User).where(User.username == username)
        return (await self.session.execute(stmt)).scalar_one_or_none()
