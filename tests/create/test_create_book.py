import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.parametrize(
    "payload, status_code",
    [
        (
            {
                "name": "QA Book",
                "author": "Boris",
                "description": "test"
            },
            200
        ),
        (
            {
                "name": "",
                "author": "Boris",
                "description": "test"
            },
            422
        ),
        (
            {
                "author": "Boris",
                "description": "test"
            },
            422
        ),
    ]
)
@pytest.mark.asyncio
async def test_create_book(payload, status_code):
    """
    Проверяем создание книги по ID через endpoint POST /books/{book_id}.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.post("/books", json=payload)

    assert response.status_code == status_code