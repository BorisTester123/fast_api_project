from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


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
            raise ValueError(422, f"Поле 'name' обязательно для заполнения")
        return v

class AuthorResponse(BaseModel):
    author_id : int = Field(examples=[1])
    name : str = Field(examples=['Максим Горький'])
    original_name: str = Field(examples=['Алексей Пешков'])
    biography : Optional[str] = Field(None, examples=['Русский писатель, просветитель'])
    composition : Optional[str] = Field(None, examples=['Война и мир'])
    model_config = ConfigDict(from_attributes=True)

class AuthorTop(BaseModel):
    authors : AuthorResponse = Field(
        default_factory=list,
        examples=[[{"author_id": 1, "name": "Пушкин"}, {"author_id": 2, "name": "Лермонтов"}]]
    )
    books_count : int

class Pagination(BaseModel):
    per_page : int = Field(ge=1, default=1, le=500000)
    page : int = Field(ge=1, le=100, default=1)


class ErrorAuth(BaseModel):
    detail : str = Field(examples=['Unauthorized'])

class ErrorMessage(BaseModel):
    detail : str = Field(examples=['Поле name обязательно для заполнения'])