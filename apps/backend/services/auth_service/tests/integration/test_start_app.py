import pytest
from auth_service.main import create_production_app
from fastapi.testclient import TestClient


def test_start_without_db():
    with pytest.raises(
        RuntimeError,
        match="Cannot establish a connection to the DB",
    ):
        app = create_production_app()
        with TestClient(app) as client:
            client.get("/")


def test_start_with_db(client: TestClient):
    client.get("/")  # Should not raise error
