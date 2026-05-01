from db.database import async_session
from db.models import Books
from db.author import Authors
from schema.schemas import BookResponse, BookCreate
from sqlalchemy import select, update, delete
from fastapi import HTTPException

class BookRepository:
    @classmethod
    async def all(cls) -> list[BookResponse]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Books))
                books = result.scalars().all()
                return [BookResponse.model_validate(book) for book in books]

    @classmethod
    async def create(cls, data: BookCreate) -> BookResponse:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Authors).where(Authors.id == data.author_id)
                )
                author = result.scalar_one_or_none()

                if not author:
                    raise HTTPException(404, f'Автор с id: {data.author_id} не найден')

                new_book = Books(
                    author_id=data.author_id,
                    name=data.name or "",
                    description=data.description or ""
                )

                session.add(new_book)
                await session.flush()
                await session.refresh(new_book)

                return BookResponse.model_validate(new_book)

    @classmethod
    async def find(cls, book_id: int) -> BookResponse:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Books).where(Books.id == book_id)
                )
                book = result.scalar_one_or_none()
        if not book:
            raise HTTPException(404, f"Книга с таким ID: {book_id} не найдена")
        return BookResponse.model_validate(book)

    @classmethod
    async def update(cls, book_id: int, data: BookCreate) -> BookResponse | None:
        async with async_session() as session:
            async with session.begin():

                book_result = await session.execute(
                    select(Books).where(Books.id == book_id)
                )

                book = book_result.scalar_one_or_none()
                if not book:
                    raise HTTPException(404, f"Книга с таким id: {book_id} не найдена")

                author_result = await session.execute(
                    select(Authors).where(Authors.id == data.author_id)
                )

                author = author_result.scalar_one_or_none()
                if not author:
                    raise HTTPException(404, f"Автор с таким id: {data.author_id} не найден")

                stmt = (
                    update(Books)
                    .where(Books.id == book_id)
                    .values(**data.model_dump())
                    .returning(Books)
                )
                result = await session.execute(stmt)
                update_book = result.scalar_one_or_none()

                return BookResponse.model_validate(update_book)

    @classmethod
    async def delete(cls, book_id: int) -> BookResponse:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Books).where(Books.id == book_id)
                )
                book = result.scalar_one_or_none()
                if not book:
                    raise HTTPException(404, f"Книга с таким ID: {book_id} не найдена")

                await session.execute(
                    delete(Books).where(Books.id == book_id)
                )
                return BookResponse.model_validate(book)