"""Authentication routes."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register() -> None:
    """Register user endpoint."""
