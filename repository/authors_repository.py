from db.author_book import author_book
from db.database import async_session
from db.author import Author
from schema.author_schema import CreateAuthor, AuthorResponse, AuthorTop
from sqlalchemy import select, update, func
from fastapi import HTTPException

class AuthorRepository:
    @classmethod
    async def all(cls) -> list[AuthorResponse]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Author))
                authors = result.scalars().all()
                return [AuthorResponse.model_validate(author) for author in authors]

    @classmethod
    async def create(cls, data: CreateAuthor):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Author).where(Author.name == data.name)
                )
                create_author = result.scalar_one_or_none()
                if create_author:
                    raise HTTPException(422, f"Автор с таким именем: {data.name} уже существует")
                author = Author(**data.model_dump())
                session.add(author)
                await session.flush()
                await session.refresh(author)
                return AuthorResponse.model_validate(author)

    @classmethod
    async def find(cls, author_id: int) -> AuthorResponse:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Author).where(Author.author_id == author_id))
                author = result.scalar_one_or_none()
            if not author:
                raise HTTPException(404, f"Автор с таким id - {author_id} не найден")

            return AuthorResponse.model_validate(author)

    @classmethod
    async def update(cls, author_id: int, data: CreateAuthor) -> AuthorResponse:
        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(Author)
                    .where(Author.author_id == author_id)
                    .values(**data.model_dump())
                    .returning(Author)
                )
                result = await session.execute(stmt)

                update_author = result.scalar_one_or_none()
            if not update_author:
                raise HTTPException(404, f"Автор с таким ID: {author_id} не найден")
            return AuthorResponse.model_validate(update_author)

    @classmethod
    async def authors_top(cls):
        async with async_session() as session:
            async with session.begin():
                books_count = func.count(author_book.c.book_id)
                result = await session.execute(
                    select(Author, books_count)
                    .join(author_book, Author.author_id == author_book.c.author_id)
                    .group_by(Author.author_id, Author.name)
                    .order_by(books_count.desc())
                    .limit(10)
                )
                author_top = result.all()
                return [AuthorTop.model_validate({
                    "authors" : [author],
                    "books_count" : count
                })
                    for author, count in author_top
                ]

    @classmethod
    async def delete(cls, author_id: int):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Author).where(Author.author_id == author_id)
                )
                author = result.scalar_one_or_none()
                await session.delete(author)
                return AuthorResponse.model_validate(author)



