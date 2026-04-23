from db.database import async_session
from db.author import Authors
from schema.schema_authors import CreateAuthor, AuthorResponse
from sqlalchemy import select, update, delete
from fastapi import HTTPException

class AuthorRepository:
    @classmethod
    async def find_all(cls) -> list[AuthorResponse]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Authors))
                authors = result.scalars().all()
                return [AuthorResponse.model_validate(author) for author in authors]

    @classmethod
    async def create(cls, data: CreateAuthor):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Authors).where(Authors.author == data.author)
                )
                create_author = result.scalar_one_or_none()
                if not create_author:
                    raise HTTPException(400, 'Поле author обязательно для заполнения')

                check_author = await session.execute(
                    select(Authors).where(Authors.author == data.author)
                )
                if check_author:
                   raise HTTPException(400, f"{data.author} уже добавлен")
                author = Authors(**data.model_dump())
                session.add(author)
                await session.flush()
                await session.refresh(author)
                return AuthorResponse.model_validate(author)

    @classmethod
    async def find_one(cls, author_id: int) -> AuthorResponse:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Authors).where(Authors.id == author_id))
                author = result.scalar_one_or_none()
            if not author:
                raise HTTPException(404, "Автор не найден")

            return AuthorResponse.model_validate(author)

    @classmethod
    async def update(cls, author_id: int, data: CreateAuthor) -> AuthorResponse:
        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(Authors)
                    .where(Authors.id == author_id)
                    .values(**data.model_dump())
                    .returning(Authors)
                )
                result = await session.execute(stmt)

                update_author = result.scalar_one_or_none()
                await session.commit()
            if not update_author:
                raise HTTPException(404, "Автор не найден")
            return AuthorResponse.model_validate(update_author)

    @classmethod
    async def delete(cls, author_id: int):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Authors).where(Authors.id == author_id)
                )
                author = result.scalar_one_or_none()

                if not author:
                    raise HTTPException(404, "Автор не найден")

                await session.execute(
                    delete(Authors).where(Authors.id == author_id)
                )

                return AuthorResponse.model_validate(author)



