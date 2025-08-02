"""Authentication service API logic."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.db.conn import check_db_health
from auth_service.di import setup_container
from auth_service.routes import auth_router


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None]:
    async with app.state.dishka_container() as request_container:
        db: AsyncSession = await request_container.get(AsyncSession)
        if not await check_db_health(db):
            raise RuntimeError("Cannot establish a connection to the DB")
    yield


def create_app() -> FastAPI:
    """Create the FastAPI application instance."""
    app = FastAPI(lifespan=_lifespan, title="Mangaluv authentication service.")
    _setup_app_routes(app)
    return app


def _setup_app_routes(app: FastAPI) -> None:
    app.include_router(auth_router)


def create_production_app() -> FastAPI:
    """Configure production FastAPI application instance."""
    app = create_app()
    container = setup_container()
    setup_dishka(container=container, app=app)
    return app
