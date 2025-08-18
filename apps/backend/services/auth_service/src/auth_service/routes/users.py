"""Authentication service users logic routes."""

from typing import Annotated

import jwt
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from auth_service.config import Settings
from auth_service.db.repositories.user import UserRepository
from auth_service.schemas.auth import User

router = APIRouter(prefix="/users", route_class=DishkaRoute)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def _get_current_user(
    token: str,
    config: Settings,
    repository: UserRepository,
) -> User:
    credentials_error = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            config.jwt.secret_key,
            algorithms=[config.jwt.algorithm],
        )
        if not (email := payload.get("sub")):
            raise credentials_error
    except InvalidTokenError as e:
        raise credentials_error from e
    if user := await repository.find_by_email(email):
        return User.model_validate(user)
    raise credentials_error


async def _get_current_active_user(current_user: User) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/me")
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    config: FromDishka[Settings],
    repository: FromDishka[UserRepository],
) -> User:
    """Return current active user."""
    user = await _get_current_user(token, config, repository)
    return await _get_current_active_user(user)
