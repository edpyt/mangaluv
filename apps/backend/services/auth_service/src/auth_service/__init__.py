from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.db.conn import check_db_health
from auth_service.di import setup_container


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator:
    async with app.state.dishka_container() as request_container:
        db = await request_container.get(AsyncSession)
        if not await check_db_health(db):
            raise RuntimeError("Cannot establish a connection to the DB")
    yield


def setup_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(lifespan=_lifespan, title="Mangaluv authentication service")
    container = setup_container()
    setup_dishka(container=container, app=app)
    return app
