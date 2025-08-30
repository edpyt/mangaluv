"""Authentication routes."""

import logging
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth.config import Settings
from auth.core.hash import (
    compute_password_hash,
    verify_password,
)
from auth.core.token import create_token_pair
from auth.db.models import User
from auth.db.repositories.user import UserRepository
from auth.schemas import auth_schemas

logger = logging.getLogger(__name__)
router = APIRouter(route_class=DishkaRoute)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register", status_code=201)
async def register(
    data: auth_schemas.UserRegister,
    repository: FromDishka[UserRepository],
) -> auth_schemas.User:
    """Register `user` route."""
    if await repository.find_by_email(data.email):
        raise HTTPException(
            status_code=400,
            detail="Email has already registered",
        )

    user_data = data.model_dump(exclude={"password_confirm"})
    user_data["password"] = compute_password_hash(user_data["password"])

    user = User(**user_data)
    # TODO: send verify email
    user.is_active = True

    if err := await repository.save(user):
        logger.exception(err)
        raise HTTPException(status_code=422, detail=repr(err))

    return auth_schemas.User.model_validate(user)


@router.post("/login")
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    repository: FromDishka[UserRepository],
    config: FromDishka[Settings],
) -> auth_schemas.UserLoginResponse:
    """Login `user` route."""
    user = await repository.find_by_username(data.username)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(status_code=403)

    token_pair = create_token_pair(
        user.email,
        access_expire_minutes=config.jwt.access_expire_minutes,
        refresh_expire_minutes=config.jwt.refresh_expire_minutes,
        secret_key=config.jwt.secret_key,
        algorithm=config.jwt.algorithm,
    )

    response.set_cookie(
        key="refresh",
        value=token_pair.refresh.token,
        expires=int(token_pair.refresh.expire.timestamp()),
        httponly=True,
    )

    return auth_schemas.UserLoginResponse(access_token=token_pair.access.token)
