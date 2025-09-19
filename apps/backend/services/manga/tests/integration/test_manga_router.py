from secrets import token_urlsafe

import pytest
from httpx import AsyncClient
from manga.infrastructure.db.models import Manga


@pytest.mark.skip("Need to add create manga route.")
async def test_get_all_mangas(
    client: AsyncClient,
    create_random_mangas: list[Manga],
):
    response = await client.get("/titles")

    assert response.status_code == 200
    assert response.json() == [
        {"id": manga.id} for manga in create_random_mangas
    ]


async def test_bad_get_manga(client: AsyncClient):
    response = await client.get("/titles/error")

    assert response.status_code == 400
    assert response.json() == {"success": False, "error": "Invalid manga ID"}

    response = await client.get("/titles/1")

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "error": "Manga with id 1 not found",
    }


async def test_get_manga(
    client: AsyncClient,
    create_random_mangas: list[Manga],
):
    manga_id = create_random_mangas[0].id

    response = await client.get(f"/titles/{manga_id}")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "manga": {"id": create_random_mangas[0].id},
    }


async def test_create_manga(client: AsyncClient):
    body = {"title": token_urlsafe()}

    response = await client.post("/titles/add/", json=body)

    assert response.status_code == 200
