from pydantic import BaseModel, ConfigDict, Field

class Author(BaseModel):
    author : str = Field(...)

class AuthorResponse(BaseModel):
    id : int = Field(examples=[1])
    author : str = (Field(examples=['Лев Толстой']))
    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    detail : str = Field(examples=['Unauthorized'])

class ErrorMessage(BaseModel):
    author : str = Field(examples=['поле author обязателен для заполнения'])