from sqlalchemy.sql.annotation import Annotated
from db.author_book import author_book
from db.database import async_session
from db.author import Author
from schema.author_schema import CreateAuthor, AuthorResponse, AuthorTop, Pagination
from sqlalchemy import select, update, func

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
                author = Author(**data.model_dump())
                session.add(result)
                await session.flush()
                await session.refresh(author)
                return AuthorResponse.model_validate(author)

    @classmethod
    async def find_one(cls, author_id: int) -> AuthorResponse:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Author).where(Author.author_id == author_id))
                author = result.scalar_one_or_none()

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
            return AuthorResponse.model_validate(update_author)

    @classmethod
    async def top(cls, pagination: Annotated[Pagination]) -> list[AuthorTop]:
        async with async_session() as session:
            async with session.begin():
                books_count = func.count(author_book.c.book_id)
                offset = (pagination.page - 1) * pagination.per_page

                query = await session.execute(
                    select(Author, books_count)
                    .join(author_book, Author.author_id == author_book.c.author_id)
                    .group_by(Author.author_id, Author.name)
                    .order_by(books_count.desc())
                    .limit(pagination.per_page)
                    .offset(offset)
                )
                top = query.all()
                return [AuthorTop.model_validate({
                    "author" : author,
                    "books_count" : count
                }) for author, count in top]

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



