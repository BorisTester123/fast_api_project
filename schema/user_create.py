from pydantic import BaseModel, Field, ConfigDict

# Создаем юзера и креды для него, которые будут храниться в БД
# для авторизации в Swagger.

class UserCreate(BaseModel):
    username : str = Field(..., min_length=8, max_length=10)
    password: str = Field(..., min_length=8, max_length=10)

# Модель, которая сверяет юзера в БД.
class UserRead(BaseModel):
    id : int
    username : str

    model_config = ConfigDict(from_attributes=True)