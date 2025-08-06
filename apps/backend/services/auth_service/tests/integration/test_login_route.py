from secrets import token_urlsafe

from auth_service.db.repositories.user import UserRepository
from dishka import AsyncContainer
from httpx import AsyncClient


async def test_bad_login_user(client: AsyncClient):
    """User not created"""
    data = {"email": "test@email.com", "password": token_urlsafe()}

    response = await client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}


async def test_login_user(client: AsyncClient, container: AsyncContainer):
    password = token_urlsafe()
    created_user = (
        # NOTE: need to refactor maybe
        await client.post(
            "/register",
            json={
                "email": f"{token_urlsafe()}@mail.com",
                "full_name": token_urlsafe(),
                "password": password,
                "password_confirm": password,
            },
        )
    ).json()
    async with container() as request_container:
        repository = await request_container.get(UserRepository)
        user = await repository.find_by_email(created_user["email"])
        user.is_active = True
        await repository.save(user)

    response = await client.post(
        "/login",
        json={
            "email": user.email,
            "password": password,
        },
    )

    assert response.status_code == 200
    assert response.cookies.get("refresh")
