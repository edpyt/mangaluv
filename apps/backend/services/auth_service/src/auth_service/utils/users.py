"""Manipulation with user model utilities."""

import jwt
from jwt.exceptions import InvalidTokenError

from auth_service.config import Settings
from auth_service.db.repositories.user import UserRepository
from auth_service.schemas.auth import User


# NOTE: maybe move to separate `errors/` directory
class CouldNotValidateCredentialsError(Exception):
    """Error for user route. Raises if bad credentials."""


async def get_current_user(
    token: str,
    config: Settings,
    repository: UserRepository,
) -> User:
    """
    Return user from db by provided token.

    :param token: JWT token
    :param config: Authentication service config
    :param repository: User DB repository
    :raises CouldNotValidateCredentialsError: If missing credentials
    :return: User schema with data from DB
    """
    try:
        payload = jwt.decode(  # pyright: ignore[reportUnknownMemberType]
            token,
            config.jwt.secret_key,
            algorithms=[config.jwt.algorithm],
        )
        if not (email := payload.get("sub")):
            raise CouldNotValidateCredentialsError()
    except InvalidTokenError as e:
        raise CouldNotValidateCredentialsError() from e
    if user := await repository.find_by_email(email):
        return User.model_validate(user)
    raise CouldNotValidateCredentialsError()
