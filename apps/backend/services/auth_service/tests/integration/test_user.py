from httpx import AsyncClient

from .types.user import CreateUserData


async def test_read_user_info(client: AsyncClient, create_user: CreateUserData):
    response = await client.get("/users/me")

    assert response.status_code == 200


async def test_unauth_read_user_info(client: AsyncClient):
    response = await client.get("/users/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
