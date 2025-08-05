from secrets import token_urlsafe

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRegisterUser:
    async def test_register_user(self, client: AsyncClient):
        _password = token_urlsafe()
        data = {
            "email": "test_user@mail.com",
            "full_name": "Test User",
            "password": _password,
            "password_confirm": _password,
        }

        response = await client.post("/register", json=data)

        assert response.status_code == 201
        assert {
            "email": data["email"],
            "full_name": data["full_name"],
        }.items() <= response.json().items()

        response = await client.post("/register", json=data)

        assert response.status_code == 400
        assert response.json() == {"detail": "Email has already registered"}

    async def test_bad_register_user(self, client: AsyncClient):
        data = {
            "email": "test_user@mail.com",
            "full_name": "Test User",
            "password": token_urlsafe(),
            "password_confirm": token_urlsafe(),
        }

        response = await client.post("/register", json=data)

        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Passwords do not match"
        )


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    _data = {}
