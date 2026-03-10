import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_update_book_by_id():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        # 1️⃣ Создаём книгу
        payload = {
            "name": "Old Book",
            "author": "Boris",
            "description": "old"
        }
        create_resp = await client.post("/books", json=payload)
        assert create_resp.status_code == 201
        book_id = create_resp.json()["book_id"]

        # 2️⃣ Обновляем книгу
        update_payload = {
            "name": "Updated Book",
            "author": "Boris Updated",
            "description": "new description"
        }
        update_resp = await client.put(f"/books/{book_id}", json=update_payload)
        assert update_resp.status_code == 200
        data = update_resp.json()

        # 3️⃣ Проверяем обновление
        assert data["book_id"] == book_id
        assert data["name"] == update_payload["name"]
        assert data["author"] == update_payload["author"]
        assert data["description"] == update_payload["description"]

        # 4️⃣ GET для проверки
        get_resp = await client.get(f"/books/{book_id}")
        assert get_resp.status_code == 200
        get_data = get_resp.json()
        assert get_data["name"] == update_payload["name"]
