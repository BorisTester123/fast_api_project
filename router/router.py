from fastapi import APIRouter, HTTPException, Path
from schema.schemas import SBookAdd, SBook
from repository.book_repository import BookRepository

router = APIRouter(
    prefix="/books",
    tags=["Книги"]
)

@router.get("", summary='Получение списка книг')
async def get_books() -> list[SBook]:
    return await BookRepository.find_all()

@router.post("", summary='Создание новой книги', status_code=201, responses={
        201: {"description": "Книга успешно создана"},
        422: {"description": "Не заполнены обязательные поля"},
    }, response_model=SBook)
async def add_book(book: SBookAdd) -> SBook:
    new_book = await BookRepository.add_one(book)
    return new_book

@router.get("/{book_id}", response_model=SBook, summary="Получение книги по ID")
async def get_book(book_id: int) -> SBook:
    book = await BookRepository.find_one(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.put("/{book_id}", response_model=SBook, summary="Изменение книги по ID", responses={
        404: {"description": "Not found"},
        422: {"description": "Не заполнены обязательные поля"},
    })
async def update_book(book_id: int, book: SBookAdd):
    updated_book = await BookRepository.update_one(book_id, book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return updated_book

@router.delete(
    "/{book_id}",
    summary="Удаление книги по ID",
    response_model=SBook
)
async def delete_book(book_id: int = Path(..., description="ID книги для удаления")):
    book = await BookRepository.find_one(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    await BookRepository.delete_one(book_id)
    return book

