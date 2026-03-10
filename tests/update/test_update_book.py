import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.parametrize(
    "update_payload, expected_status",
    [
        ({"name": "Updated Book", "author": "Boris"}, 200),
        ({"name": ""}, 422),
        ({"name" : "Программируем на Python",
          "author" : "Michael Dawson",
          "description" : "Программируем играючи"}, 200)
    ]
)
@pytest.mark.asyncio
async def test_update_book(update_payload, expected_status):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # Сначала создаём книгу, чтобы был ID
        create_resp = await client.post("/books", json={"name": "Temp", "author": "Boris", "description": "tmp"})
        book_id = create_resp.json()["book_id"]

        response = await client.put(f"/books/{book_id}", json=update_payload)

    assert response.status_code == expected_status
    header = response.headers
    assert header.get("content-type") == "application/json"

    if expected_status == 200:
        data = response.json()
        for key, value in update_payload.items():
            assert data.get(key) == value
