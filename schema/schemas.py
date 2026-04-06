from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BookCreate(BaseModel):
    name: str = Field(..., max_length=130)
    author: Optional[str] = Field(None, max_length=130)
    description: Optional[str] = Field(None, max_length=130)

# Модель для описания Response.
class BookResponse(BaseModel):
    id: int = Field(..., examples=["1"])
    name: str = Field(..., examples=["Война и мир"])
    author: str = Field(None, examples=["Лев Толстой"])
    description: str = Field(
    examples=["«Война и мир» — роман Льва Толстого, написанный в 1863–1869 годах. Жанр — роман-эпопея."])
    model_config = ConfigDict(from_attributes=True)

# Описание моделей для разных статусов кодов.
class ErrorResponse(BaseModel):
    name: str = Field(..., examples=["Поле name обязательно для заполнения"])

class ErrorMessage(BaseModel):
    detail: str = Field(..., examples=["Unauthorized"])