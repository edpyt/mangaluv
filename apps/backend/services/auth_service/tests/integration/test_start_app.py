import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_start_without_db(app: FastAPI):
    with pytest.raises(
        RuntimeError,
        match="Cannot establish a connection to the DB",
    ):
        with TestClient(app) as client:
            client.get("/")


def test_start_with_db(client: TestClient):
    client.get("/")  # Should not raise error
