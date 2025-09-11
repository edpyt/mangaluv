from httpx import AsyncClient


async def test_get_manga(client: AsyncClient):
    response = await client.get("/1")

    assert response.status_code == 200
