from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from configuration import settings
from sqlalchemy import text

async_engine = create_async_engine(
    settings.database_url_asyncpg,
    pool_pre_ping = True,
    pool_recycle = 300
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Model(DeclarativeBase):
    pass

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS books CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS authors CASCADE;"))