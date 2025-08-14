from secrets import token_urlsafe

from httpx import AsyncClient

from .types.user import CreateUserData


async def test_bad_login_user(client: AsyncClient):
    data = {"email": "test@email.com", "password": token_urlsafe()}

    response = await client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}


async def test_login_user(client: AsyncClient, create_user: CreateUserData):
    response = await client.post("/login", json=create_user)

    assert response.status_code == 200
    assert response.cookies.get("refresh")
