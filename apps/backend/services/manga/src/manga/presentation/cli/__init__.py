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
    engine = create_engine(db_uri)
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as con:
        title: str = Prompt.ask(":pencil: Enter manga title")
        description: str = Prompt.ask(":pencil: Enter manga description")
        con.execute(
            insert(table).values(
                {
                    "id": uuid4(),  # FIXME: should be default level on db level
                    "title": title,
                    "description": description,
                }
            )
        )

    secho("New manga was added", fg="green")


if __name__ == "__main__":
    app()
