from httpx import AsyncClient

from .types.user import CreateUserData


async def test_logout_user(client: AsyncClient, create_user: CreateUserData):
    await client.post("/login", json=create_user)
    await client.post("/logout")
