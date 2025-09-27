from secrets import token_urlsafe

from manga.presentation.cli import app
from typer.testing import CliRunner


def test_add_manga(runner: CliRunner):
    title, description, image = (
        token_urlsafe(),
        token_urlsafe(),
        "https://static.wikia.nocookie.net/weeky-shonen-jump/images/b/ba/Sakamoto_Days_WSJ_Volume_1.png/revision/latest?cb=20210329150102",
    )

    result = runner.invoke(app, input="\n".join([title, description, image]))

    assert result.exit_code == 0
