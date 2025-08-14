from httpx import AsyncClient

from .types.user import CreateUserData


async def test_read_user_info(client: AsyncClient, create_user: CreateUserData):
    _response = await client.get("/users/me")
