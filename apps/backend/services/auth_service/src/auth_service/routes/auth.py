"""Authentication routes."""

import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException

from auth_service.core.hash import compute_password_hash
from auth_service.db.models import User
from auth_service.db.repositories.user import UserRepository
from auth_service.schemas import auth_schemas

logger = logging.getLogger(__name__)
router = APIRouter(route_class=DishkaRoute)


@router.post("/register", status_code=201)
async def register(
    data: auth_schemas.UserRegister,
    repository: FromDishka[UserRepository],
) -> auth_schemas.User:
    """Register user endpoint."""
    if await repository.find_by_email(data.email):
        raise HTTPException(
            status_code=400,
            detail="Email has already registred",
        )

    user_data = data.model_dump(exclude={"password_confirm"})
    user_data["password"] = compute_password_hash(user_data["password"])

    user = User(**user_data)
    if err := await repository.save(user):
        logger.exception(err)
        raise HTTPException(status_code=422, detail=repr(err))

    # TODO: send verify email

    return auth_schemas.User.model_validate(user)
