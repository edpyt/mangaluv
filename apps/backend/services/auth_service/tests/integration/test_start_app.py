import pytest
from fastapi.testclient import TestClient


def test_startup_without_db() -> None:
    from src.auth_service import app

    with pytest.raises(RuntimeError, match="Can't connect to DB."):
        with TestClient(app) as client:
            client.get("/")
