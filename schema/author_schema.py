from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Annotated
from fastapi import Query


class CreateAuthor(BaseModel):
    name : str = Field(..., max_length=100)
    original_name : str = Field(..., max_length=100)
    biography : Optional[str] = Field(None, max_length=100)
    composition : Optional[str] = Field(None, max_length=100)
    birth_date : str
    death_date : str = Field(None)

    @field_validator("name")
    @classmethod
    def check_author(cls, v):
        if not v or not v.strip():
            raise ValueError(422, "Поле 'name' обязательно для заполнения")
        return v

    @field_validator('birth_date')
    @classmethod
    def check_date(cls, v):
        if not v or not v.strip():
            raise ValueError(422, "Поле 'birth_date' обязательно для заполнения")
        return v

class AuthorResponse(BaseModel):
    author_id : int = Field(examples=[1])
    name : str = Field(examples=['Максим Горький'])
    original_name: str = Field(examples=['Алексей Пешков'])
    biography : Optional[str] = Field(None, examples=['Русский писатель, просветитель'])
    composition : Optional[str] = Field(None, examples=['Война и мир'])
    birth_date : Optional[str] = Field(..., examples=['DD.MM.YYYY'])
    death_date : Optional[str] = Field(None, examples=['DD.MM.YYYY'])
    model_config = ConfigDict(from_attributes=True)

class AuthorTop(BaseModel):
    authors : AuthorResponse = Field(
        default_factory=list,
        examples=[[{"author_id": 1, "name": "Пушкин"}, {"author_id": 2, "name": "Лермонтов"}]]
    )
    books_count : int

class Pagination(BaseModel):
    per_page : int = Field(ge=1, default=1, le=25)
    page : int = Field(ge=1, le=100, default=1)

async def get_pagination(
    page: Annotated[int, Query(ge=1, description="Номер страницы")] = 1,
    per_page: Annotated[int, Query(ge=1, le=25, description="Записей на странице")] = 10
) -> Pagination:
    return Pagination(page=page, per_page=per_page)

class ErrorAuth(BaseModel):
    detail : str = Field(examples=['Unauthorized'])

class ErrorMessage(BaseModel):
    detail : str = Field(examples=['Поле name обязательно для заполнения'])