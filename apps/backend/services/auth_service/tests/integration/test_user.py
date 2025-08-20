from httpx import AsyncClient

from .types.user import CreateUserData


async def test_unauth_read_user_info(client: AsyncClient):
    response = await client.get("/users/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


async def test_read_user_info(client: AsyncClient, create_user: CreateUserData):
    token = (
        await client.post(
            "/login",
            json=create_user,
        )
    ).json()["access_token"]

    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["is_active"]
    assert response_data["email"] == create_user["email"]
    assert response_data["full_name"] == create_user["full_name"]
