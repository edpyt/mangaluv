import pytest
from api_gateway import app
from fastapi.testclient import TestClient


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)
