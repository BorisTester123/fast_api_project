from pydantic import BaseModel, ConfigDict, Field

class CreateAuthor(BaseModel):
    author : str = Field(..., max_length=100)
    biography : str = Field(None, max_length=100)
    composition : str = Field(None, max_length=100)

class AuthorResponse(BaseModel):
    id : int = Field(examples=[1])
    author : str = (Field(examples=['Лев Толстой']))
    biography : str = Field(examples=['Русский писатель, просветитель'])
    composition : str = (Field(examples=['Война и мир']))
    model_config = ConfigDict(from_attributes=True)

class ErrorAuth(BaseModel):
    detail : str = Field(examples=['Unauthorized'])

class ErrorMessage(BaseModel):
    author : str = Field(examples=['поле author обязателен для заполнения'])