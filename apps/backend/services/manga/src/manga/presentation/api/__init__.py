from robyn import Robyn


def start_app(host: str = "127.0.0.1", port: int = 8080):
    """Startup application."""
    app = setup_app()
    app.start(host, port)


def setup_app() -> Robyn:
    """Return Robyn application."""
    app = Robyn(__file__)
    _setup_sub_routers(app)
    _setup_di(app)
    return app


def _setup_sub_routers(app: Robyn) -> None:
    from manga.presentation.api.manga import router as manga_router

    app.include_router(manga_router)


def _setup_di(app: Robyn) -> None:
    ...
    # TODO::
    # app.inject_global(sqla_engine=create_async_engine())
