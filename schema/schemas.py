from pydantic import BaseModel, ConfigDict, Field, field_validator

class BookCreate(BaseModel):
    author_id: int
    name: str = Field(None, max_length=130)
    description: str = Field(None, max_length=130)

    @field_validator("author_id")
    def check_author(cls, author):
        if not author:
            raise ValueError("Поле author_id не может быть отрицательным")
        return author
# Модель для описания Response.
class BookResponse(BaseModel):
    id: int = Field(..., examples=["1"])
    author_id: int = Field(..., examples=["Автор"])
    name: str = Field(None, examples=["Война и мир"])
    description: str = Field(
    examples=["«Война и мир» — роман Льва Толстого, написанный в 1863–1869 годах. Жанр — роман-эпопея."])
    model_config = ConfigDict(from_attributes=True)

# Описание моделей для разных статусов кодов.
class ErrorResponse(BaseModel):
    name: str = Field(..., examples=["Поле name обязательно для заполнения"])

class ErrorMessage(BaseModel):
    detail: str = Field(..., examples=["Unauthorized"])