from pydantic import BaseModel, ConfigDict, field_validator

# 🔹 Входная модель (создание книги)
class SBookAdd(BaseModel):
        name: str
        title: str = ""
        description: str = ""

        @field_validator("title", "description")
        @classmethod
        def check_not_empty(cls, v: str, info):
            if not v.strip():
                raise ValueError(f"Поле '{info.field_name}' не может быть пустым")
            return v



# 🔹 Модель для чтения книги
class SBook(SBookAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


# 🔹 Модель ответа с id (для POST/PUT/DELETE)
class SBookId(BaseModel):
    ok: bool
    book_id: int
