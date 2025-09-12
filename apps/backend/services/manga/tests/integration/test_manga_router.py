from httpx import AsyncClient


async def test_get_manga(client: AsyncClient):
    response = await client.get("/1")

    assert response.status_code == 200


async def test_bad_get_manga(client: AsyncClient):
    response = await client.get("/error")

    assert response.status_code == 400
    assert response.json()["error"] == "Provided bad manga id"
