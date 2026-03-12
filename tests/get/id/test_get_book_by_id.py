import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from enums.enum import GlobalMessageErrors


@pytest.mark.asyncio
async def test_get_book_by_id():
    """
    Проверяем получение книги по ID через endpoint GET /books/{book_id}.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        # создаём книгу
        payload = {
            "name": "Test Book",
            "author": "Boris",
            "description": "test"
        }

        create_response = await ac.post("/books", json=payload)

        # Проверяем статус код созданной книги.
        assert create_response.status_code == 201
        book_data = create_response.json()
        book_id = book_data["book_id"]

        # получаем книгу по id
        response = await ac.get(f"/books/{book_id}")
        assert response.status_code == 200, GlobalMessageErrors.WRONG_STATUS_CODE.value
        header = response.headers
        assert header.get("content-type") == "application/json"


        # в каком формате приходят данные и headers

        data = response.json()

        for key, value in data.items():
            assert key in data
            assert data[key] == value


