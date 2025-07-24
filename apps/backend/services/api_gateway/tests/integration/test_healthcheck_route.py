import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_health_check(api_client: TestClient) -> None:
    response = api_client.get("/healthcheck")

    assert response.status_code == 200

    msg = response.json()["message"]

    assert msg == "OK"
