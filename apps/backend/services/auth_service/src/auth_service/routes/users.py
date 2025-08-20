"""Authentication service users logic routes."""

from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer

from auth_service.config import Settings
from auth_service.db.repositories.user import UserRepository
from auth_service.schemas.auth import User
from auth_service.utils.users import (
    CouldNotValidateCredentialsError,
    get_current_user,
)

router = APIRouter(prefix="/users", route_class=DishkaRoute)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Set up [exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#reuse-fastapis-exception-handlers).

    For `users` router.

    :param app: FastAPI instance
    """

    async def _could_not_validate_credentials_error(*_) -> None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    app.exception_handler(CouldNotValidateCredentialsError)(
        _could_not_validate_credentials_error  # pyright: ignore[reportUnknownArgumentType]
    )


@router.get("/me")
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    config: FromDishka[Settings],
    repository: FromDishka[UserRepository],
) -> User:
    """Return current active user."""
    user = await get_current_user(token, config, repository)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
