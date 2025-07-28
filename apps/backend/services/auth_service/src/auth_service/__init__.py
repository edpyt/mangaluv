from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.db.conn import check_db_health
from auth_service.di import setup_container


@asynccontextmanager
async def _lifespan(_: FastAPI) -> AsyncGenerator:
    container = setup_container()
    async with container() as request_container:
        db = await request_container.get(AsyncSession)
        if not await check_db_health(db):
            raise RuntimeError("Cannot establish a connection to the DB")
    yield


# FIXME: separate function to setup app
app = FastAPI(lifespan=_lifespan)
