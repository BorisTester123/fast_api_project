from pydantic import BaseModel, ConfigDict, field_validator

# 🔹 Входная модель (создание книги)
class SBookAdd(BaseModel):
        name: str
        title: str = ""
        description: str = ""

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str, info):
            v_clean = v.strip()
            if not v_clean:
                raise ValueError(f"Поле '{info.field_name}' не может быть пустым")
            if len(v_clean) > 20:
                raise ValueError(f"Поле '{info.field_name}' не может быть длиннее 20 символов")
            return v_clean



# 🔹 Модель для чтения книги
class SBook(SBookAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


# 🔹 Модель ответа с id (для POST/PUT/DELETE)
class SBookId(BaseModel):
    ok: bool
    book_id: int
