import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_get_books():
    """
    Проверяем, что endpoint получения списка книг
    успешно отвечает (200 OK) и возвращает список книг в формате JSON
    """

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        response = await ac.get("/books")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

