from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class CreateAuthor(BaseModel):
    name : str = Field(..., max_length=100)
    biography : Optional[str] = Field(None, max_length=100)
    composition : Optional[str] = Field(None, max_length=100)

    @field_validator("name")
    @classmethod
    def check_author(cls, v):
        if not v:
            raise ValueError("поле name обязательно для заполнения")
        return v

class AuthorResponse(BaseModel):
    id : int = Field(examples=[1])
    name : str = (Field(examples=['Лев Толстой']))
    biography : Optional[str] = Field(None, examples=['Русский писатель, просветитель'])
    composition : Optional[str] = Field(None, examples=['Война и мир'])
    model_config = ConfigDict(from_attributes=True)


class ErrorAuth(BaseModel):
    detail : str = Field(examples=['Unauthorized'])

class ErrorMessage(BaseModel):
    author : str = Field(examples=['поле author обязателен для заполнения'])