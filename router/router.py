# Импортируем класс APIRouter для создания API endpoints
from fastapi import APIRouter, HTTPException, Depends
# Импортируем модель данных для работы с книгами
from schema.schemas import BookResponse, BookCreate, ErrorResponse, ErrorMessage
# Импортируем репозиторий для работы с книгами
from repository.book_repository import BookRepository
# Импортируем из файла авторизации функцию check BasicAuth.
from BasicAuth.check_authorization import check_auth

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
                       "description" : "Не авторизован",
                       "model" : ErrorMessage,
                    },
            },
            response_model=list[BookResponse],
            dependencies=[Depends(check_auth)])
# Асинхронная функция для получения списка книг
async def get_books():
    # возвращаем из репозитория все книги из базы данных
    return await BookRepository.find_all()

@router.post("", summary='Создание новой книги', status_code=201,
             responses={
                    422: {
                      "description": "Не заполнены обязательные поля",
                      "model": ErrorResponse
                },
                    401:
                    {
                       "description" : "Не авторизован",
                       "model" : ErrorMessage,
                    }
            },
            response_model=BookResponse,
            dependencies=[Depends(check_auth)])
async def create_book(book: BookCreate) -> BookResponse:
    if not book:
        raise ValueError("автор не найден")
    return await BookRepository.create(book)

@router.get("/{book_id}", summary="Получение книги по ID",
            responses={
                401:
                    {
                        "description" : "Не авторизован",
                        "model" : ErrorMessage,
                    },
            },
            response_model=BookResponse,
            dependencies=[Depends(check_auth)])
async def get_book(book_id: int):
    # ищем книгу по ID в базе данных
    book = await BookRepository.find_one(book_id)
    # Проверяем если книги в базе нет
    if not book:
        # Если книги в базе данных нет возвращаем ошибку
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.put("/{book_id}",summary="Изменение книги по ID",
            responses={
                422:
                    {
                      "description": "Не заполнены обязательные поля",
                      "model": ErrorResponse,
            },
                401:
                    {
                      "description" : "Не авторизован",
                      "model" : ErrorMessage,
                    },
            },
            response_model=BookResponse,
            dependencies=[Depends(check_auth)])
async def update_book(book_id: int, book: BookCreate):
    # Отправляем запрос в базу данных на обновление книги
    updated_book = await BookRepository.update_one(book_id, book)
    # Если книги в базе данных нет
    if not updated_book:
        # Возвращаем ошибку о том, что книга не найдена
        raise HTTPException(status_code=404, detail="Книга не найдена")
    # Иначе обновляем книгу в базе данных
    return updated_book

@router.delete("/{book_id}", summary="Удаление книги по ID",
               responses={
                   422:
                       {
                           "description": "Не заполнены обязательные поля",
                           "model": ErrorResponse
                       },
                   401:
                       {
                           "description" : "Не авторизован",
                           "model" : ErrorMessage,
                       },
               },
               response_model=BookResponse,
               dependencies=[Depends(check_auth)])
async def delete_book(book_id: int):
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

