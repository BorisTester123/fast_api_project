from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "sqlite+aiosqlite:///books.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class BooksOrm(Model):
        __tablename__ = 'books'

        id : Mapped[int] = mapped_column(primary_key=True)
        name : Mapped[str]
        title: Mapped[str]
        description : Mapped[str | None]


async def create_tables():
    async with engine.connect() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.connect() as conn:
        await conn.run_sync(Model.metadata.drop_all)