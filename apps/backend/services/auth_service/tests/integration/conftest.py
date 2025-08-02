import os
from collections.abc import Generator

import pytest
from auth_service.main import setup_app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def db() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:16.9-bookworm") as postgres:
        yield postgres


@pytest.fixture
def app() -> FastAPI:
    return setup_app()


@pytest.fixture
def client(db: PostgresContainer, app: FastAPI) -> Generator[TestClient]:
    os.environ["DB__uri"] = db.get_connection_url().replace(
        "postgresql+psycopg2", "postgresql+asyncpg"
    )
    with TestClient(app) as client:
        yield client
    del os.environ["DB__uri"]
