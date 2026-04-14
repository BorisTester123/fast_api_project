import pytest
from fastapi.testclient import TestClient
from main import app
from router.router_auth import get_db
from db.database import async_session
import os
from dotenv import load_dotenv
from enums.enum import GlobalMessageErrors

load_dotenv()
USERNAME = os.getenv("ADMIN_USERNAME")
PASSWORD = os.getenv("ADMIN_PASSWORD")

# Асинхронная сессия для тестов с автоматическим откатом
async def override_get_db_for_tests():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
# фикстура для создания клиента.
@pytest.fixture(scope="module")
def client():
    # Переопределяем зависимость БД только на время работы фикстуры
    app.dependency_overrides[get_db] = override_get_db_for_tests
    with TestClient(app, base_url="http://test") as c:
        c.auth = (USERNAME, PASSWORD)  # Basic Auth для всех запросов
        yield c
    # Очищаем переопределения после тестов
    app.dependency_overrides.clear()

@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"name": "developer Python", "author": "Boris", "description": "test"}, 201),
        ({"name": "", "author": "Boris", "description": "test"}, 422),
        ({"author": "Boris", "description": "test"}, 400),
    ], GlobalMessageErrors.WRONG_ELEMENT_COUNT
)
def test_create_book(client, payload, expected_status):
    test_payload = payload.copy()
    # auth уже установлен в фикстуре, явно передавать не нужно
    response = client.post("/books", json=test_payload)

    assert response.status_code == expected_status, \
        f"Ожидали {expected_status}, получили {response.status_code}. Payload: {test_payload}"

    if expected_status == 201:
        data = response.json()
        for key, value in payload.items():
            assert key in data
            assert data[key] == value