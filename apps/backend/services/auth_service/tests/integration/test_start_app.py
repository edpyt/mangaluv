import pytest
from auth_service.main import create_production_app
from fastapi.testclient import TestClient
from httpx import AsyncClient


def test_start_without_db():
    with pytest.raises(
        RuntimeError,
        match="Cannot establish a connection to the DB",
    ):
        app = create_production_app()
        with TestClient(app) as client:
            client.get("/")


@pytest.mark.asyncio
async def test_start_with_db(client: AsyncClient):
    await client.get("/")  # Should not raise error
