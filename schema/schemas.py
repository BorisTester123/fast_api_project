from pydantic import BaseModel, ConfigDict, Field

# Класс для валидации полей в API
class SBook(BaseModel):
    id: int = Field(examples=["1"])
    name: str = Field(..., examples=["Война и мир"])
    author: str = Field(None, max_length=250, examples=["Лев Толстой"])
    description: str = Field(None, max_length=250,
    examples=["«Война и мир» — роман Льва Толстого, написанный в 1863–1869 годах. Жанр — роман-эпопея."])
    model_config = ConfigDict(from_attributes=True)

class SBookAdd(BaseModel):
    name: str
    author: str = Field(None, max_length=130)
    description: str = Field(None, max_length=130)

class ErrorResponse(BaseModel):
    name: str = Field(..., examples=["Поле name обязательно для заполнения"])