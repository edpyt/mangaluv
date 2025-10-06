"""Manga service command-line interface."""

from typing import Annotated
from uuid import uuid4

from rich.prompt import Prompt
from sqlalchemy import MetaData, Table, create_engine, insert
from typer import Option, Typer, secho

app = Typer()
metadata = MetaData()


@app.command()
def add_manga(
    db_uri: Annotated[
        str, Option(help="Manga service database URI.")
    ] = "postgresql+psycopg://postgres:password@localhost:5432/manga_db",
    table_name: Annotated[str, Option()] = "manga",
):
    """Add new manga to the storage."""
    with create_engine(db_uri).connect() as con:  # NOTE: check connection first
        title: str = Prompt.ask(":pencil: Enter manga title")
        description: str = Prompt.ask(":pencil: Enter manga description\n")
        table = Table(table_name, metadata, autoload_with=con)
        con.execute(
            insert(table).values(
                {
                    "id": uuid4(),
                    "title": title,
                    "description": description,
                }
            )
        )

    secho("New manga was added", fg="green")


if __name__ == "__main__":
    app()
