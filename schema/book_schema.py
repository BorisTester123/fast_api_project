from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List
from schema.author_schema import AuthorResponse

class BookCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=130)
    description: Optional[str] = Field(None, max_length=130)
    author_ids: List[int] = Field(..., examples=[[1,2]])

class BookResponse(BaseModel):
    book_id: int = Field(..., examples=["1"])
    title: Optional[str] = Field(None, examples=["Евгений Онегин"])
    description: Optional[str] = Field(None, examples=["«Евгений Онегин» — роман в стихах...»"])
    authors: List[AuthorResponse] = Field(
        default_factory=list,
        examples=[[{"author_id": 1, "name": "Пушкин"}]]
    )

    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    title: str = Field(..., examples=["Поле author_id обязательно для заполнения"])

class ErrorMessage(BaseModel):
    detail: str = Field(..., examples=["Unauthorized"])