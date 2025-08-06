from secrets import token_urlsafe

import pytest
from auth_service.db.repositories.user import UserRepository
from dishka import AsyncContainer
from httpx import AsyncClient


async def test_bad_login_user(client: AsyncClient):
    """User not created"""
    data = {"email": "test@email.com", "password": token_urlsafe()}

    response = await client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.parametrize(
    "create_user_data",
    [
        {
            "email": "test@mail.com",
            "full_name": "test",
            "password": "test",
        },
        {
            "email": f"{token_urlsafe()}@mail.com",
            "full_name": token_urlsafe(),
            "password": token_urlsafe(),
        },
    ],
)
async def test_login_user(
    client: AsyncClient,
    container: AsyncContainer,
    create_user_data: dict[str, str],
):
    create_user_data["password_confirm"] = create_user_data["password"]
    created_user = (
        # NOTE: need to refactor maybe
        await client.post("/register", json=create_user_data)
    ).json()
    async with container() as request_container:
        repository = await request_container.get(UserRepository)
        if not (user := await repository.find_by_email(created_user["email"])):
            raise
        user.is_active = True
        await repository.save(user)

    response = await client.post("/login", json=create_user_data)

    assert response.status_code == 200
    assert response.cookies.get("refresh")
