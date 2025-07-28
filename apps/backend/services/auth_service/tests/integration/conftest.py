import pytest
from auth_service import setup_app
from fastapi import FastAPI


@pytest.fixture
def app() -> FastAPI:
    return setup_app()
