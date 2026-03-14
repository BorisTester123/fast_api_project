from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from configuration import settings

# Создаём асинхронный движок
async_engine = create_async_engine(
    settings.database_url_asyncpg,
    echo=False
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

# Функции создания/удаления таблиц
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)