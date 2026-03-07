from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

# Модель для получения данных
class SBook(BaseModel):
    id: int
    name: Optional[str]
    author: Optional[str]
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)

# Модель для обновления данных
class SBookAdd(BaseModel):
    name: Optional[str]
    author: Optional[str]
    description: Optional[str]
    """
    Проверяем что поле "name" не может быть пустым.
    """
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Поле 'name' не может быть пустым")
        return v

class SBookId(BaseModel):
    book_id: int
    name: Optional[str] | None
    author: Optional[str] | None
    description: Optional[str] | None