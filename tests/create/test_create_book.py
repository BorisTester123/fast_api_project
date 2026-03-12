import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"name": "QA Book", "author": "Boris", "description": "test"}, 201),
        ({"name": "", "author": "Boris", "description": "test"}, 422),
        ({"author": "Boris"}, 422),
    ]
)
@pytest.mark.asyncio
async def test_create_book(payload, expected_status):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.post("/books", json=payload)

    assert response.status_code == expected_status
    header = response.headers
    assert header.get("content-type") == "application/json"

    if expected_status == 201:
        data = response.json()
        for key, value in payload.items():
            assert key in data
            assert data[key] == value