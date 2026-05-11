from sqlalchemy.orm import selectinload
from enums.enum import CountryCode
from algoritm_isbn import generate_isbn13
from db.database import async_session
from db.books import Book
from db.author import Author
from schema.book_schema import BookResponse, BookCreate
from sqlalchemy import select
from fastapi import HTTPException

class BookRepository:
    @classmethod
    async def all(cls) -> list[BookResponse]:
        async with (async_session() as session):
            async with session.begin():
                result = await session.execute(
                    select(Book)
                    .options(selectinload(Book.authors)))
                books = result.unique().scalars().all()
                return [BookResponse.model_validate(book) for book in books]

    @classmethod
    async def create(cls, data: BookCreate) -> BookResponse:
        async with async_session() as session:
            async with session.begin():
                author_result = await session.execute(
                    select(Author).where(Author.author_id.in_(data.author_ids))
                )
                authors = author_result.scalars().all()
                if len(authors) != len(data.author_ids):
                    raise HTTPException(
                        404,
                        f"Авторы с такими id - {data.author_ids} не найдены"
                    )

                book_result = await session.execute(
                    select(Book)
                    .options(selectinload(Book.authors))
                    .where(Book.title == data.title)
                )
                existing_book = book_result.scalars().all()
                if existing_book:
                    raise HTTPException(422, f'Книга с таким названием: {data.title} уже существует')

                result_book = Book(
                    isbn=generate_isbn13(),
                    title=data.title,
                    description=data.description or "",
                    language_code=CountryCode.RU,
                    authors=authors,
                    publication_date=data.publication_date
                    )
                session.add(result_book)
                await session.flush()
                book_with_authors = await session.scalar(
                    select(Book)
                    .options(selectinload(Book.authors))
                    .where(Book.book_id == result_book.book_id)
                )
                return BookResponse.model_validate(book_with_authors)

    @classmethod
    async def find(cls, book_id: int) -> BookResponse:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Book)
                    .options(selectinload(Book.authors))
                    .where(Book.book_id == book_id)
                )
                book = result.scalar_one_or_none()
        if not book:
            raise HTTPException(404, f"Книга с таким ID: {book_id} не найдена")
        return BookResponse.model_validate(book)

    @classmethod
    async def update(cls, book_id: int, data: BookCreate) -> BookResponse:
        async with async_session() as session:
            async with session.begin():
                book_result = await session.execute(
                    select(Book)
                    .options(selectinload(Book.authors))
                    .where(Book.book_id == book_id)
                )

                book = book_result.scalar_one_or_none()

                if not book:
                    raise HTTPException(404, f"Книга с таким id: {book_id} не найдена")

                author_result = await session.execute(
                    select(Author).where(
                        Author.author_id.in_(data.author_ids)
                    )
                )
                authors = author_result.scalars().all()

                if len(authors) != len(data.author_ids):
                    raise HTTPException(404, f"Авторы с таким id: {data.author_ids} не найдены")

                book_title = await session.execute(
                    select(Book).where(Book.title == data.title)
                )
                result = book_title.scalar_one_or_none()

                if result:
                    raise HTTPException(422, f'Книга с таким названием - {data.title} уже существует')

                book.title = data.title
                book.description = data.description
                book.authors = authors
                await session.flush()
                await session.refresh(book, attribute_names=['authors'])
                return BookResponse.model_validate(book)

    @classmethod
    async def delete(cls, book_id: int) -> BookResponse:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Book)
                    .options(selectinload(Book.authors))
                    .where(Book.book_id == book_id)
                )

                book = result.scalar_one_or_none()

                if not book:
                    raise HTTPException(404, f"Книга с id: {book_id} не найдена")

                authors = list(book.authors)

                book_response = BookResponse(
                    book_id=book.book_id,
                    isbn=generate_isbn13(),
                    title=book.title,
                    description=book.description,
                    language_code=CountryCode.RU.FR.US,
                    authors=authors,
                    publication_date=book.publication_date
                )

                await session.delete(book)
                await session.flush()

                return book_response