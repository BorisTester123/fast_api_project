from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from fastapi import Query
from schema.author_schema import AuthorResponse, CreateAuthor, ErrorMessage, ErrorAuth, AuthorTop, Pagination
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
                        "description" : "Unauthorized",
                        "model" : ErrorAuth
                    }
            },
            response_model=list[AuthorResponse],
            dependencies = [Depends(check_auth)])
async def all():
    return await AuthorRepository.all()

@router.post("", summary="Создание нового автора", status_code=201,
             responses={
                 401:
                     {
                         "description" : "Неавторизован",
                         "model" : ErrorAuth
                     },
                 422:
                     {
                         "description" : "Не заполнены обязательные поля",
                         "model" : ErrorMessage
                     },
             },
             response_model=AuthorResponse,
             dependencies=[Depends(check_auth)])
async def create(author: CreateAuthor):
    return await AuthorRepository.create(author)

async def get_pagination(
    page: Annotated[int, Query(ge=1, description="Номер страницы")] = 1,
    per_page: Annotated[int, Query(ge=1, le=500000, description="Записей на странице")] = 10
) -> Pagination:
    return Pagination(page=page, per_page=per_page)

@router.get("/top", summary="Получение списка топ 10 авторов по количеству книг",
            responses={
                401:
                    {
                        "description" : "Unauthorized",
                        "model" : ErrorAuth
                    }
            },
            response_model=list[AuthorTop],
            dependencies=[Depends(check_auth)])
async def top(pagination: Annotated[Pagination, Depends(get_pagination)]):
    return await AuthorRepository.top(pagination)

@router.get("/{author_id}", summary="Получения автора по ID",
            responses={
                401:
                    {
                        "description" : "Неавторизован",
                        "model" : ErrorAuth
                    }
            },
            response_model=AuthorResponse,
            dependencies=[Depends(check_auth)])
async def find(author_id: int):
    author = await AuthorRepository.find(author_id)
    if not author:
        raise HTTPException(404, "Автор не найден")
    return author

@router.put("/{author_id}", summary="Изменение автора по ID", status_code=200,
            responses={
                401:
                    {
                        "description" : "Unauthorized",
                        "model" : ErrorAuth
                    },
                422:
                    {
                        "description" : "Не заполнены обязательные поля",
                        "model" : ErrorMessage
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
                           "model" : ErrorAuth
                       },
                   422:
                       {
                           "description" : "Не заполнены обязательные поля",
                           "model" : ErrorMessage
                       }
               },
               response_model=AuthorResponse,
               dependencies=[Depends(check_auth)])
async def delete(author_id: int):
    author = await AuthorRepository.find(author_id)
    if not author:
        raise HTTPException(404, f"Автор с таким ID: {author_id} не найден")
    await AuthorRepository.delete(author_id)
    return author