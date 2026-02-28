from db.database import new_session, BooksOrm
from schema.schemas import SBookAdd, SBook
from sqlalchemy import select

class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd) -> int:
        async with new_session() as session:
            book_dict = data.model_dump()

            book = BooksOrm(**book_dict)
            session.add(book) # добавляем объект в сессию, все изменения отправятся в БД
            await session.flush()
            await session.commit()
            return book.id

    @classmethod
    async def find_all(cls) -> list[SBook] :
        async with new_session() as session:
            query = select(BooksOrm)
            result = await session.execute(query)
            book_models = result.scalars().all()
            book_schemas = [SBook.model_validate(book_models)for book_models in book_models]
            return book_schemas
