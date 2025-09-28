"""Manga service command-line interface."""

from typing import Annotated

from rich.prompt import Prompt
from sqlalchemy import create_engine, text
from typer import Option, Typer, secho

app = Typer()


@app.command()
def add_manga(
    db_uri: Annotated[str, Option(help="Manga service database URI.")],
    manga_tablename: Annotated[str, Option()] = "manga",
):
    """Add new manga to the storage."""
    with create_engine(db_uri).connect() as con:
        title: str = Prompt.ask(":pencil: Enter manga title")
        description: str = Prompt.ask(":pencil: Enter manga description")
        con.execute(
            text("INSERT INTO :manga_table VALUES :title,:description"),
            {
                "manga_table": manga_tablename,
                "title": title,
                "description": description,
            },
        )
    secho("New manga was added", fg="green")


if __name__ == "__main__":
    app()
