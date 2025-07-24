import pytest_asyncio
from fastapi.testclient import TestClient
from src.api_gateway import app


@pytest_asyncio.fixture
async def api_client() -> TestClient:
    return TestClient(app)
