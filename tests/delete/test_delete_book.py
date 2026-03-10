import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_delete_book_by_id():
    """
    Проверяем удаление книги по ID через endpoint DELETE /books/{book_id}.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        # 1️⃣ Создаём книгу
        payload = {
            "name": "Book to Delete",
            "author": "Boris",
            "description": "test"
        }

        create_response = await client.post("/books", json=payload)
        assert create_response.status_code == 201
        book_data = create_response.json()
        book_id = book_data["book_id"]

        # 2️⃣ Проверяем, что GET возвращает книгу
        get_response = await client.get(f"/books/{book_id}")
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data["book_id"] == book_id

        # 3️⃣ Удаляем книгу
        delete_response = await client.delete(f"/books/{book_id}")
        assert delete_response.status_code == 204

        # 4️⃣ Проверяем, что GET теперь возвращает 404
        get_after_delete = await client.get(f"/books/{book_id}")
        assert get_after_delete.status_code == 404
