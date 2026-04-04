from db.database import create_tables, delete_tables
import pytest

# Сначала запускаем этот файл для того, чтобы создать таблицу и удалить данные из нее.
@pytest.fixture()
async def lifespan():
    await delete_tables()
    await create_tables()
    yield
    print("Приложение выключается")