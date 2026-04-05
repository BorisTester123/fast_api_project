from db.database import async_session
from db.models import BooksOrm
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
                result = await session.execute(select(BooksOrm))
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
                # Проверяем, есть ли уже книга с таким названием
                result = await session.execute(
                    select(BooksOrm).where(BooksOrm.name == data.name)
                )
                # возьми единственный объект, если он есть, иначе None, но если их несколько — ошибка.
                existing_book = result.scalar_one_or_none()
                #  если такая книга с таким названием уже есть
                if existing_book:
                    # добавляем описание ошибки
                    raise HTTPException(
                        status_code=400,
                        detail=f"Книга с названием '{data.name}' уже существует"
                    )

                # Если книги с таким названием нет — создаём новую
                book = BooksOrm(**data.model_dump())
                # добавляем книгу в базу данных
                session.add(book)
                # Отправь все изменения в базу данных
                await session.flush()
                await session.refresh(book)  # загружает актуальные значения из БД
                # возвращаем книгу согласно нашей модели
                return BookResponse.model_validate(book)

    @classmethod
    # создание асинхронной функции, в которой передается в query params book_id
    async def find_one(cls, book_id: int) -> BookResponse | None:
        # создаем новую сессию
        async with async_session() as session:
            async with session.begin():
                # Если книга с таким id есть → вернёт объект Book
                result = await session.execute(
                    select(BooksOrm).where(BooksOrm.id == book_id)
                )
                book = result.scalar_one_or_none()
                # если книга в базе данных есть.
            if book:
                # возвращаем книгу и валидируем согласно нашей модели Pydantic
                return BookResponse.model_validate(book)
            # иначе возвращаем None
            return None

    @classmethod
    async def update_one(cls, book_id: int, data: BookCreate) -> BookResponse | None:
        # создаем новую сессию
        async with async_session() as session:
            # обновляем книгу по id в нашей таблице books, и возвращаем обновленный словарь нашей книги, и его обновленные значения
            async with session.begin():
                stmt = (
                    update(BooksOrm)
                    .where(BooksOrm.id == book_id)
                    .values(**data.model_dump())
                    .returning(BooksOrm)
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
                    select(BooksOrm).where(BooksOrm.id == book_id)
                )
                book = result.scalar_one_or_none()
                if not book:
                    return None

                # Удаляем книгу из базы данных
                await session.execute(
                    delete(BooksOrm).where(BooksOrm.id == book_id)
                )
                return BookResponse.model_validate(book)