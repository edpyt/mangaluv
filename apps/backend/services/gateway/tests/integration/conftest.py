import pytest
from fastapi.testclient import TestClient
from gateway import app


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)
