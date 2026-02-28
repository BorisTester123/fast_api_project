from fastapi import APIRouter, HTTPException
from schema.schemas import SBookAdd, SBook, SBookId
from repository.repository import BookRepository

router = APIRouter(
    prefix="/books",
    tags=["Книги"]
)

@router.get("", summary='Получение списка книг')
async def get_books() -> list[SBook]:
    return await BookRepository.find_all()

@router.post("", summary='Создание новой книги')
async def add_book(book: SBookAdd) -> SBookId:
    book_id = await BookRepository.add_one(book)
    return SBookId(ok=True, book_id=book_id)

@router.get("/{id}", summary='Получение книги по ID')
async def get_book_by_id(book_id: int) -> SBook:
    book = await BookRepository.find_one(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.put("/{id}", summary="Изменение книги по ID")
async def update_book(book_id: int, book: SBookAdd) -> SBookId:
    updated = await BookRepository.update_one(book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return SBookId(ok=True, book_id=book_id)

@router.delete("/{id}", summary='Удаление книги по ID')
async def delete_book(book_id: int) -> SBookId:
    deleted = await BookRepository.delete_one(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return SBookId(ok=True, book_id=book_id)
