from fastapi import APIRouter, HTTPException, Depends
from schema.schemas import SBookAdd, SBook, ErrorResponse, ErrorMessage
from repository.book_repository import BookRepository
from auth.authorization import verify_credentials

# Создаем роутер для группировки endpoints связанных с операциями
router = APIRouter(
    # Присваиваем тэг и префикс для нашей документации API
    prefix="/books",
    tags=["Книги"]
)

@router.get("", summary='Получение списка книг',
            responses={
                401:
                    {
                        "description": "Неверная авторизация",
                        "model": ErrorMessage,
                    },
            },
            response_model=list[SBook],
            dependencies=[Depends(verify_credentials)])

# Асинхронная функция для получения списка книг
async def get_books() -> list[SBook]:
    # возвращаем из репозитория все книги из базы данных
    return await BookRepository.find_all()

@router.post("", summary='Создание новой книги', status_code=201,
             responses={
                 422:
                     {
                         "description": "Не заполнены обязательные поля",
                         "model": ErrorResponse
                    },
                 401:
                     {
                         "description": "Неверная авторизация",
                         "model": ErrorMessage,
                     },
             },
             response_model=SBook,
             dependencies=[Depends(verify_credentials)])
async def create_book(book: SBookAdd) -> SBook:
    # Создаем новую книгу и отправляем данные о книге в базу данных
    book = await BookRepository.create(book)
    # Возвращаем созданную книгу
    return book

@router.get("/{id}", summary="Получение книги по ID",
            responses={
                401:
                    {
                        "description": "Неверная авторизация",
                        "model": ErrorMessage,
                    },
            },
            response_model=SBook,
            dependencies=[Depends(verify_credentials)])
async def get_book(book_id: int) -> SBook:
    # ищем книгу по ID в базе данных
    book = await BookRepository.find_one(book_id)
    # Проверяем если книги в базе нет
    if not book:
        # Если книги в базе данных нет возвращаем ошибку
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.put("/{id}",summary="Изменение книги по ID",
            responses={
                422:
                    {
                        "description": "Не заполнены обязательные поля",
                        "model": ErrorResponse
                    },
                401:
                    {
                        "description": "Неверная авторизация",
                        "model": ErrorMessage,
                    },
            },
            response_model = SBook,
            dependencies = [Depends(verify_credentials)])
async def update_book(book_id: int, book: SBookAdd):
    # Отправляем запрос в базу данных на обновление книги
    updated_book = await BookRepository.update_one(book_id, book)
    # Если книги в базе данных нет
    if not updated_book:
        # Возвращаем ошибку о том, что книга не найдена
        raise HTTPException(status_code=404, detail="Книга не найдена")
    # Иначе обновляем книгу в базе данных
    return updated_book

@router.delete("/{id}", summary="Удаление книги по ID",
               responses={
                   422:
                       {
                           "description": "Не заполнены обязательные поля",
                           "model": ErrorResponse
                       },
                   401:
                       {
                           "description": "Неверная авторизация",
                           "model": ErrorMessage,
                       },
               },
               response_model=SBook,
               dependencies=[Depends(verify_credentials)])
async def delete_book(book_id: int) -> SBook:
    # ищем книгу в базе данных
    book = await BookRepository.find_one(book_id)
    # если книги в базе данных нет
    if not book:
        # возвращаем ошибку о том, что книги нет
        raise HTTPException(status_code=404, detail="Книга не найдена")
    # удаляем книгу из базы данных
    await BookRepository.delete_one(book_id)
    # возвращаем удаленную книгу
    return book

