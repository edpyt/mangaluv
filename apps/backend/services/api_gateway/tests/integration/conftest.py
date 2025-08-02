import pytest
from fastapi.testclient import TestClient
from src.api_gateway import app


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)
