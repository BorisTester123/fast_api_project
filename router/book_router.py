from fastapi import APIRouter, HTTPException, Depends
from schema.book_schema import BookResponse, BookCreate, ErrorResponse, ErrorMessage
from repository.book_repository import BookRepository
from BasicAuth.check_authorization import check_auth
router = APIRouter(
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
async def get_books():
    return await BookRepository.all()

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
async def create_book(book: BookCreate):
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
    book = await BookRepository.find(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Книга с таким id: {book_id} не найдена")
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
    updated_book = await BookRepository.update(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail=f"Книга с таким id: {book_id} не найдена")
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
    book = await BookRepository.find(book_id)
    await BookRepository.delete(book_id)
    return book

