from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    data = {
        "email": "test_user@mail.com",
        "full_name": "Test User",
        "password": "testpass123",
        "password_confirm": "321",  # NOTE: different passwords
    }

    response = client.post("/register", json=data)

    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Passwords do not match"
    )

    data["password_confirm"] = data["password"]

    response = client.post("/register", json=data)

    assert response.status_code == 201
