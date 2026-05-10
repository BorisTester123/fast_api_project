from fastapi import APIRouter, HTTPException, Depends
from schema.author_schema import AuthorResponse, CreateAuthor,ErrorMessage, ErrorAuth
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
async def get_authors():
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
async def create_author(author: CreateAuthor):
    return await AuthorRepository.create(author)

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
async def get_one_author(author_id: int):
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