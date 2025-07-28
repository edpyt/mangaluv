import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer


def test_start_without_db(app: FastAPI) -> None:
    with pytest.raises(
        RuntimeError,
        match="Cannot establish a connection to the DB",
    ):
        with TestClient(app) as client:
            client.get("/")


def test_start_with_db(app: FastAPI) -> None:
    with PostgresContainer("postgres:16.9-bookworm") as postgres:
        psql_url = postgres.get_connection_url()
        os.environ["DB__url"] = psql_url.replace(
            "postgresql+psycopg2", "postgresql+asyncpg"
        )
        with TestClient(app) as client:
            client.get("/")
