import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    data = {
        "email": "test_user@mail.com",
        "full_name": "Test User",
        "password": "testpass123",
        "password_confirm": "321",  # NOTE: different passwords
    }

    response = await client.post("/register", json=data)

    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Passwords do not match"
    )

    data["password_confirm"] = data["password"]

    response = await client.post("/register", json=data)

    assert response.status_code == 201

    response_json = response.json()

    assert response_json["email"] == data["email"]
    assert response_json["full_name"] == data["full_name"]

    response = await client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Email has already registred"}
