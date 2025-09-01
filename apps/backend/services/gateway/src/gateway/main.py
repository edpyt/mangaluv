"""Main package API Gateway service."""

from fastapi import FastAPI


def setup_app() -> FastAPI:
    """Return API application instance."""
    app = FastAPI()
    _setup_routers(app)
    return app


def _setup_routers(app: FastAPI) -> None:
    from gateway.routes.healthcheck import router as health_router

    app.include_router(health_router)
