from manga.presentation.cli import app
from typer.testing import CliRunner


def test_add_manga(runner: CliRunner):
    title, description = (
        "Sakamoto Days",
        "Manga series written and illustrated by Yuto Suzuki.",
    )

    result = runner.invoke(app, input="\n".join([title, description]))

    assert result.exit_code == 0
