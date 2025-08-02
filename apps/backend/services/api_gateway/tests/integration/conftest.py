from fastapi.testclient import TestClient
from src.api_gateway import app


def api_client() -> TestClient:
    return TestClient(app)
