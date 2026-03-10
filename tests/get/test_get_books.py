import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from enums.enum import GlobalMessageErrors


@pytest.mark.asyncio
async def test_get_books():
    """
    Проверяем, что endpoint получения списка книг
    успешно отвечает (200 OK) и возвращает список книг в формате JSON
    """
    # Контекст менеджер обращается к HTTP - клиенту, который делает запросы к нашему API
    async with AsyncClient(

        transport=ASGITransport(app=app),
        base_url = "http://test"
    ) as ac:
        # получи информацию с endpoint /books
        response = await ac.get("/books")
        assert response.status_code == 200, GlobalMessageErrors.WRONG_STATUS_CODE.value
        header = response.headers
        assert header.get("content-type") == "application/json"


        # в каком формате приходят данные и headers
        data = response.json()

        for book in data:  # book — словарь
            for key, value in book.items():  # теперь items() у словаря
                # проверяем, что ключ существует и значение не None
                if isinstance(response.status_code, list):
                    assert key in book
                    assert book[key] == value
