from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List
from schema.author_schema import AuthorResponse
from enums.enum import CountryCode
from datetime import datetime, date


class BookCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=130)
    description: Optional[str] = Field(None, max_length=130)
    language_code : List[CountryCode]
    author_ids: List[int] = Field(..., examples=[[1, 2]])
    publication_date: Optional[date] = Field(..., examples=["05.05.1976"])

    @field_validator('publication_date', mode='before')
    @classmethod
    def parse_publication_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%d.%m.%Y").date()
        return v

class BookResponse(BaseModel):
    book_id: int = Field(..., examples=["1"])
    isbn: str = Field(..., min_length=13, max_length=17, examples=["9785171183660"])
    title: Optional[str] = Field(None, examples=["Евгений Онегин"])
    description: Optional[str] = Field(None, examples=["«Евгений Онегин» — роман в стихах...»"])
    language_code: Optional[CountryCode] = Field(..., examples=["RU"])
    authors: List[AuthorResponse] = Field(
        default_factory=list,
        examples=[[{"author_id": 1, "name": "Пушкин"}, {"author_id": 2, "name": "Лермонтов"}]]
    )
    publication_date: Optional[date] = Field(..., examples=["05.05.1976"])

    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    title: str = Field(..., examples=["Поле author_id обязательно для заполнения"])

class ErrorMessage(BaseModel):
    detail: str = Field(..., examples=["Unauthorized"])