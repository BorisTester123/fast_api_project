from fastapi import APIRouter, HTTPException, Path
from schema.schemas import SBookAdd, SBook, SBookUpdate
from repository.book_repository import BookRepository

router = APIRouter(
    prefix="/books",
    tags=["Книги"]
)

@router.get("", summary='Получение списка книг')
async def get_books() -> list[SBook]:
    return await BookRepository.find_all()

@router.post("", summary='Создание новой книги', status_code=201)
async def add_book(book: SBookAdd) -> SBook:
    id_book = await BookRepository.add_one(book)

    return SBook(
        id=id_book,
        name=book.name,
        author=book.author,
        description=book.description
    )

@router.get("/{book_id}", response_model=SBook, summary="Получение книги по ID")
async def get_book(book_id: int):
    book = await BookRepository.find_one(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return SBook(
        id=book.id,
        name=book.name,
        author=book.author,
        description=book.description
    )


@router.put("/{book_id}", summary="Изменение книги по ID")
async def update_book(book_id: int, book: SBookAdd) -> SBookUpdate:
    updated = await BookRepository.update_one(book_id, book)

    if not updated:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    return SBookUpdate(
        id=updated,
        name=book.name,
        author=book.author,
        description=book.description
    )


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

