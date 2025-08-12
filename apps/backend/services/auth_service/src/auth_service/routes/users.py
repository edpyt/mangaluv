"""Authentication service users logic routes."""

from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/users", route_class=DishkaRoute)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/me")
async def current_user():
    """Return current active user."""


async def _get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
