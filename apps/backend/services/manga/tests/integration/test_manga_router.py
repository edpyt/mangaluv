from re import match

from httpx import AsyncClient
from manga.infrastructure.db.models import Manga


async def test_bad_get_manga(client: AsyncClient):
    response = await client.get("/title/error")

    assert response.status_code == 400
    assert response.text == "Provided bad manga id"

    response = await client.get("/title/1")

    assert response.status_code == 404
    assert match(r"Manga.+not\sfound.+", response.text)


async def test_get_manga(
    client: AsyncClient,
    create_random_mangas: list[Manga],
):
    manga_id = create_random_mangas[0].id

    response = await client.get(f"/title/{manga_id}")

    assert response.status_code == 200
    assert response.json()["id"] == manga_id
