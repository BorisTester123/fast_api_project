from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class BookCreate(BaseModel):
    author_id: int
    name: Optional[str] = Field(None, max_length=130)
    description: Optional[str] = Field(None, max_length=130)

class BookResponse(BaseModel):
    id: int = Field(..., examples=["1"])
    author_id: int = Field(..., examples=["1"])
    name: Optional[str] = Field(None, examples=["Евгений Онегин"])
    description: Optional[str] = Field(None,
    examples=["«Евгений Онегин» — роман в стихах русского поэта А. С. Пушкина."])
    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    name: str = Field(..., examples=["Поле author_id обязательно для заполнения"])

class ErrorMessage(BaseModel):
    detail: str = Field(..., examples=["Unauthorized"])