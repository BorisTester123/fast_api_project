import pytest
from fastapi.testclient import TestClient
from main import app
from router.router_auth import get_db
from db.database import async_session
import os
from dotenv import load_dotenv

# Используем креды для авторизации из .env файла
load_dotenv()
USERNAME = os.getenv("ADMIN_USERNAME")
PASSWORD = os.getenv("ADMIN_PASSWORD")

# Создаем вторичную асинхронную сессию (чтобы не конфликтовало с основной)
async def override_get_db_for_tests():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
# связываем их между собой
app.dependency_overrides[get_db] = override_get_db_for_tests

# Фикстура, то что будет выполнено до начала тестирования, наши предусловия
# Перед тем как запускать тесты, сначала авторизуемся.
@pytest.fixture(scope="module")
def client():
    with TestClient(app, base_url="http://test") as c:
        c.auth = (USERNAME, PASSWORD)
        yield c

# Декоратор для параметризации тестов, тестируем сразу несколько сценариев
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"name": "123321", "author": "Boris", "description": "test"}, 201),   # success
        ({"name": "", "author": "Boris", "description": "test"}, 422),    # empty name → 422
        ({"author": "Boris", "description": "test"}, 422),                # 400 поле name обязательно для заполнения
    ],
)

# функция принимает себя фикстуру и асинхронного клиента
def test_update_book(client, payload, expected_status):
    # делаем копию
    test_payload = payload.copy()
    update_response = client.post("/books", json=test_payload)
    book_id = update_response.json()["book_id"]

    response = client.put(f"/books/{book_id}", json=payload)

    assert response.status_code == expected_status, \
        f"Ожидали {expected_status}, получили {response.status_code}. Payload: {test_payload}"

    assert response.status_code == expected_status
    header = response.headers
    assert header.get("content-type") == "application/json"

    # если наш статус код == 201, проходимся по нашему JSON (ключ - значение) в payload
    # и проверяем (assert) содержится ли ключ в нашем json
    # в нашем словаре ищем ключ и == нашему значению
    if expected_status == 200:
        data = response.json()
        for key, value in payload.items():
            assert data.get(key) == value