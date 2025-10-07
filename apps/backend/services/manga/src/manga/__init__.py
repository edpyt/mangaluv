from litestar import Litestar, get


@get("/")
def index() -> str:
    """Hello."""
    return "Hello,World!"


app = Litestar([index])
