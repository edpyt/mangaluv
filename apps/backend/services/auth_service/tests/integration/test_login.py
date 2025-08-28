from secrets import token_urlsafe

from httpx import AsyncClient

from .types.user import CreateUserData


async def test_bad_login_user(client: AsyncClient):
    data = {"username": "bob", "password": token_urlsafe()}

    response = await client.post("/login", data=data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}


async def test_login_user(client: AsyncClient, create_user: CreateUserData):
    response = await client.post(
        "/login",
        data={
            "username": create_user["username"],
            "password": create_user["password"],
        },
    )

    assert response.status_code == 200
    assert response.cookies.get("refresh")
