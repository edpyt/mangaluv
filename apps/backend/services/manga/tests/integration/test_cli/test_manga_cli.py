from secrets import token_urlsafe

from manga.presentation.cli import app
from typer.testing import CliRunner


def test_add_manga(runner: CliRunner):
    title, description, vol, chapter = (
        token_urlsafe(),
        token_urlsafe(),
        "1",
        "1",
    )

    _result = runner.invoke(
        app,
        input="\n".join([title, description, vol, chapter]),
    )
