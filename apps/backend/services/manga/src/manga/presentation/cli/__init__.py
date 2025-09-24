"""Manga service command-line interface."""

from rich.prompt import Prompt
from typer import Typer

app = Typer()


@app.command()
def add_manga():
    """Add new manga to the storage."""
    title: str = Prompt.ask(":pencil: Enter manga title")
    description: str = Prompt.ask(":pencil: Enter manga description")
    vol: str = Prompt.ask(":pencil: Enter manga volume")
    chapter: str = Prompt.ask(":pencil: Enter manga chapter")
    print(title, description, vol, chapter)  # noqa: T201


if __name__ == "__main__":
    app()
