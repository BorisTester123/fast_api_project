from db.database import new_session, BooksOrm
from schema.schemas import SBookAdd, SBook
from sqlalchemy import select, update, delete

class BookRepository:

    @classmethod
    async def add_one(cls, data: SBookAdd) -> int:
        async with new_session() as session:
            book_dict = data.model_dump()
            book = BooksOrm(**book_dict)
            session.add(book)
            await session.flush()
            await session.commit()
            return book.id

    @classmethod
    async def find_all(cls) -> list[SBook]:
        async with new_session() as session:
            result = await session.execute(select(BooksOrm))
            books = result.scalars().all()
            return [SBook.model_validate(book) for book in books]

    @classmethod
    async def find_one(cls, book_id: int) -> SBook | None:
        async with new_session() as session:
            result = await session.execute(select(BooksOrm).where(BooksOrm.id == book_id))
            book = result.scalar_one_or_none()
            if book:
                return SBook.model_validate(book)
            return None

    @classmethod
    async def update_one(cls, book_id: int, data: SBookAdd) -> bool:
        async with new_session() as session:
            stmt = (
                update(BooksOrm)
                .where(BooksOrm.id == book_id)
                .values(**data.model_dump())
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0  # True если что-то обновилось

    @classmethod
    async def delete_one(cls, book_id: int) -> bool:
        async with new_session() as session:
            stmt = delete(BooksOrm).where(BooksOrm.id == book_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
