"""Manga service command-line interface."""

from rich.prompt import Prompt
from typer import Typer

app = Typer()


@app.command()
def add_manga():
    """Add new manga to the storage."""
    title: str = Prompt.ask(":pencil: Enter manga title")
    description: str = Prompt.ask(":pencil: Enter manga description")
    image_cover: str = Prompt.ask(":camera: Enter image cover")
    print(title, description, image_cover)  # noqa: T201 # TODO: remove this `print`


if __name__ == "__main__":
    app()
