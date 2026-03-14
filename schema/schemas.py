from pydantic import BaseModel, ConfigDict, field_validator

class SBook(BaseModel):
    id: int
    name: str
    author: str | None = None
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)

    @field_validator("name")
    def name_not_empty(cls, value):
        if value is None or value.strip() == "":
            raise ValueError("Название книги обязательно")
        return value

class SBookAdd(BaseModel):
    name: str | None = None
    author: str | None = None
    description: str | None = None
