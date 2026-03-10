import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_get_book_by_id():
    """
    Проверяем получение книги по ID через endpoint GET /books/{book_id}.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        # создаём книгу
        payload = {
            "name": "Test Book",
            "author": "Boris",
            "description": "test"
        }

        create_response = await client.post("/books", json=payload)

        # Проверяем статус код созданной книги.

        assert create_response.status_code == 201

        book_data = create_response.json()

        book_id = book_data["book_id"]

        # получаем книгу по id
        response = await client.get(f"/books/{book_id}")

        assert response.status_code == 200

        data = response.json()

        # проверяем, что ответ, который приходит от сервера, имеет такую структуру.
        assert data["book_id"] == book_id
        assert data["name"] == payload["name"]
        assert data["author"] == payload["author"]
        assert data["description"] == payload["description"]

        # негативные сценарии теста.
        assert data["book_id"] == book_id
        assert data["name"] == payload["username"]
        assert data["author"] == payload["fdjsfjds"]
        assert data["description"] == payload[""]

