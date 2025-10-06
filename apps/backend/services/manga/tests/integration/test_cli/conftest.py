import pytest
from typer.testing import CliRunner


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    return CliRunner()
