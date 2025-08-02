"""Authentication routes."""

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth_service.schemas import auth_schemas

router = APIRouter(route_class=DishkaRoute)


@router.post("/register", status_code=201)
async def register(
    data: auth_schemas.UserRegister,
    db: FromDishka[AsyncSession],
) -> str:
    """Register user endpoint."""
    print(data)

    return "Hello, World"
