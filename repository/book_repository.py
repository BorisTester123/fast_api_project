from db.database import async_session
from db.models import Books
from schema.schemas import BookResponse, BookCreate
from sqlalchemy import select, update, delete
from fastapi import HTTPException

class BookRepository:
    @classmethod
    async def find_all(cls) -> list[BookResponse]:
        # создаем сессию.
        async with async_session() as session:
            # контекстный менеджер транзакции, выполняет все команды, если ошибка rollback, иначе commit
            async with session.begin():
                # отправляем запрос в базу данных, ищем наши книги
                result = await session.execute(select(Books))
                # все книги найдены
                books = result.scalars().all()
                # валидируем все полученные книги из базы данных согласно нашей модели
                return [BookResponse.model_validate(book) for book in books]

    @classmethod
    async def create(cls, data: BookCreate) -> BookResponse:
        # создаем новую сессию
        async with async_session() as session:
            # контекстный менеджер транзакции
            async with session.begin():
                result = await session.execute(
                    select(Books).where(Books.author_id == data.author_id)
                )
                check_author = result.scalar_one_or_none()
                if not check_author:
                    raise HTTPException(404, f'Автор не найден')

                authors_id = await session.execute(
                    select(Books).where(Books.author_id == data.author_id)
                )
                if authors_id:
                    raise HTTPException(400, f"Книга с таким {data.author_id} уже существует")
                # Если книги с таким названием нет — создаём новую
                book = Books(**data.model_dump())
                # добавляем книгу в базу данных
                session.add(book)
                # Отправь все изменения в базу данных
                await session.flush()
                await session.refresh(book)  # загружает актуальные значения из БД
                # возвращаем книгу согласно нашей модели
                return BookResponse.model_validate(book)

    @classmethod
    # создание асинхронной функции, в которой передается в query params book_id
    async def find_one(cls, book_id: int) -> BookResponse:
        # создаем новую сессию
        async with async_session() as session:
            async with session.begin():
                # Если книга с таким id есть → вернёт объект Book
                result = await session.execute(
                    select(Books).where(Books.id == book_id)
                )
                book = result.scalar_one_or_none()
                # если книга в базе данных есть.
        if not book:
            # если в базе данных такой книги нет, кидаем ошибку
            raise HTTPException(404, detail="Книга не найдена")
        # иначе валидируем модель
        return BookResponse.model_validate(book)

    @classmethod
    async def update_one(cls, book_id: int, data: BookCreate) -> BookResponse | None:
        # создаем новую сессию
        async with async_session() as session:
            # обновляем книгу по id в нашей таблице books, и возвращаем обновленный словарь нашей книги, и его обновленные значения
            async with session.begin():
                stmt = (
                    update(Books)
                    .where(Books.id == book_id)
                    .values(**data.model_dump())
                    .returning(Books)
                )
                # отправь запрос в базу данных
                result = await session.execute(stmt)

                # находим один объект и обновляем его
                updated_book = result.scalar_one_or_none()  # вернёт объект или None
                await session.commit()

                if updated_book is None:
                    return None
                # возвращаем модель и валидируем наш полученный объект
                return BookResponse.model_validate(updated_book)

    @classmethod
    async def delete_one(cls, book_id: int) -> BookResponse | None:
        # асинхронная сессия и присваиваем название сессии
        async with async_session() as session:
            async with session.begin():
                # Отправляем запрос в сессии и ищем в таблице одну запись по id
                result = await session.execute(
                    select(Books).where(Books.id == book_id)
                )
                book = result.scalar_one_or_none()
                if not book:
                    return None

                # Удаляем книгу из базы данных
                await session.execute(
                    delete(Books).where(Books.id == book_id)
                )
                return BookResponse.model_validate(book)