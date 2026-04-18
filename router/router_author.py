from fastapi import APIRouter, HTTPException, Depends
from schema.schema_authors import AuthorResponse, CreateAuthor, ErrorResponse, ErrorMessage
from repository.authors_repository import AuthorRepository
from BasicAuth.check_authorization import check_auth

router = APIRouter(
    prefix="/authors",
    tags=["Авторы"]
)

@router.get("", summary="Получения списка авторов",
            responses={
                401:
                    {
                        "description" : "Неавторизован",
                        "model" : ErrorMessage
                    }
            },
            response_model=list[AuthorResponse],
            dependencies = [Depends(check_auth)])
async def get_authors():
    return await AuthorRepository.find_all()

@router.post("", summary="Создание нового автора",
             responses={
                 401:
                     {
                         "description" : "Неавторизован",
                         "model" : ErrorMessage
                     },
                 422:
                     {
                         "description" : "Не заполнены обязательные поля",
                         "model" : ErrorResponse
                     },
             },
             response_model=AuthorResponse,
             dependencies=[Depends(check_auth)])
async def create_book(book: CreateAuthor):
    return await AuthorRepository.create(book)

@router.get("/{author_id}", summary="Получения автора по ID",
            responses={
                401:
                    {
                        "description" : "Неавторизован",
                        "model" : ErrorMessage
                    }
            },
            response_model=AuthorResponse,
            dependencies=[Depends(check_auth)])
async def get_book_one(author_id: int):
    author = await AuthorRepository.find_one(author_id)
    if not author:
        raise HTTPException(404, "Автор не найден")
    return author

@router.put("/{author_id}", summary="Изменение автора по ID",
            responses={
                401:
                    {
                        "description" : "Unauthorized",
                        "model" : ErrorMessage
                    },
                422:
                    {
                        "description" : "Не заполнены обязательные поля",
                        "model" : ErrorResponse
                    }
            },
            response_model=AuthorResponse,
            dependencies=[Depends(check_auth)])
async def update(author_id: int, author: CreateAuthor):
    update_author = await AuthorRepository.update(author_id, author)
    if not update_author:
        raise HTTPException(404, "Автор не найден")
    return update_author

@router.delete("/{author_id}", summary="Удаление автора по ID",
               responses={
                   401:
                       {
                           "description" : "Unauthorized",
                           "model" : ErrorMessage
                       },
                   422:
                       {
                           "description" : "Не заполнены обязательные поля",
                           "model" : ErrorResponse
                       }
               },
               response_model=AuthorResponse,
               dependencies=[Depends(check_auth)])
async def delete(author_id: int):
    author = await AuthorRepository.find_one(author_id)
    if not author:
        raise HTTPException(404, "Автор не найден")
    await AuthorRepository.delete(author_id)
    return author