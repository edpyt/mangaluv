from fastapi.testclient import TestClient


def test_health_check(api_client: TestClient) -> None:
    response = api_client.get("/healthcheck")

    assert response.status_code == 200
