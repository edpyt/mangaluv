"""Manga service command-line interface."""

from typing import Annotated

from typer import Option, Typer

app = Typer()


@app.command()
def add_manga(
    title: Annotated[str, Option(help="Manga title")],
    description: Annotated[str, Option(help="Manga description")],
    volume: Annotated[int, Option()],
    chapter: Annotated[int, Option()],
):
    """Add new manga to the storage."""


if __name__ == "__main__":
    app()
