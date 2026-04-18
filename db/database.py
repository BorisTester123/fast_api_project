from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from configuration import settings
from sqlalchemy import text

# Создаём асинхронный движок
async_engine = create_async_engine(
    settings.database_url_asyncpg,
    pool_pre_ping = True,
    pool_recycle = 300
)

# Сессии
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс
class Model(DeclarativeBase):
    pass

# Асинхронная функция создания таблицы в БД
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
# Асинхронная функция для удаления таблицы в БД
async def delete_tables():
    async with async_engine.begin() as conn:
        # Удаляем данные в связанной таблице.
        await conn.execute(text("DROP TABLE IF EXISTS books CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS authors CASCADE;"))