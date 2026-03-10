import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from schema.schemas import SBook


@pytest.mark.asyncio
async def test_delete_book():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # Создаём книгу
        create_resp = await client.post(
            "/books",
            json={"name": "Temp", "author": "Boris", "description": "tmp"}
        )
        book_id = create_resp.json()["book_id"]

        # Удаляем книгу
        delete_resp = await client.delete(f"/books/{book_id}")
        assert delete_resp.status_code == 200

        # Проверка через Pydantic модель
        deleted_book = SBook(**delete_resp.json())
        assert deleted_book.id == book_id
        assert deleted_book.name == "Temp"
        assert deleted_book.author == "Boris"

        # Проверяем, что GET вернёт 404
        get_resp = await client.get(f"/books/{book_id}")
        assert get_resp.status_code == 404

