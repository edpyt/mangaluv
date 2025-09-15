from re import match

from httpx import AsyncClient

# TODO:
# async def test_get_manga(client: AsyncClient): ...


async def test_bad_get_manga(client: AsyncClient):
    response = await client.get("/error")

    assert response.status_code == 400
    assert response.json()["error"] == "Provided bad manga id"

    response = await client.get("/1")

    assert response.status_code == 404
    assert match(r"Manga.+not\sfound.+", response.text)
