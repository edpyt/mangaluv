"""Authentication routes."""

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.schemas import auth_schemas

router = APIRouter(route_class=DishkaRoute)


@router.post("/register", status_code=201)
async def register(
    _data: auth_schemas.UserRegister,
    _db: FromDishka[AsyncSession],
) -> str:
    """Register user endpoint."""
    return "Hello, World"
