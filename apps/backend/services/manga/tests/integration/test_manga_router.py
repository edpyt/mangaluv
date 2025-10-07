from uuid import uuid4

from httpx import AsyncClient
from manga.infrastructure.db.models import Manga


async def test_get_all_mangas(
    client: AsyncClient,
    create_random_mangas: list[Manga],
):
    response = await client.get("/titles")

    assert response.status_code == 200
    assert response.json() == {
        "titles": [
            {
                "id": str(manga.id),
                "description": manga.description,
                "title": manga.title,
            }
            for manga in create_random_mangas
        ],
        "total": len(create_random_mangas),
    }


async def test_bad_get_manga(client: AsyncClient):
    response = await client.get("/titles/error")

    assert response.status_code == 400
    assert response.json() == {"success": False, "error": "Invalid manga ID"}

    unexpected_uuid = uuid4()
    response = await client.get(f"/titles/{unexpected_uuid}")

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "error": f"Manga with id {unexpected_uuid} not found",
    }


async def test_get_manga(
    client: AsyncClient,
    create_random_mangas: list[Manga],
):
    manga = create_random_mangas[0]

    response = await client.get(f"/titles/{manga.id}")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "manga": {
            "id": str(manga.id),
            "title": manga.title,
            "description": manga.description,
        },
    }
