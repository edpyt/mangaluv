import pytest
from fastapi.testclient import TestClient
from gateway.main import setup_app


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(setup_app())
