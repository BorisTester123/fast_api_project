import pytest
from fastapi.testclient import TestClient
from main import app
from BasicAuth.authorization import get_db
from db.database import async_session
import os
from dotenv import load_dotenv
from enums.enum import GlobalMessageErrors

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
        ({"name": "Программируем на Python",
          "author": "Michael D",
          "description": "Обучение языку программирования"
          },
            201
        ),   # success
    ],
)

# функция принимает себя фикстуру и асинхронного клиента
def test_get_by_id_book(client, payload, expected_status):
    # создаем нашу книгу POST /books
    create_response = client.post("/books", json=payload)
    # получаем Response от сервера
    book_data = create_response.json()

    # отправляем запрос на получение книги по id
    response = client.get(f"/books")
    # проверяем что статус код == 200 или опрокидываем ошибку из Enums.
    assert response.status_code == 200, GlobalMessageErrors.WRONG_STATUS_CODE.value
    header = response.headers
    assert header.get("content-type") == "application/json"

    assert response.status_code == expected_status, \
        f"Ожидали {expected_status}, получили {response.status_code}. Payload: {payload}"

    # если наш статус код == 200, проходимся по нашему JSON (ключ - значение) в payload
    # и проверяем (assert) содержится ли ключ в нашем json
    # в нашем словаре ищем ключ и == нашему значению
    if expected_status == 200:
        data = response.json()
        for key, value in data.items():
            assert key in data
            assert data[key] == value