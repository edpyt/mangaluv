from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    response = client.get("/auth/register")

    assert response.status_code == 401
