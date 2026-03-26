from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    username : str = Field(..., min_length=8, max_length=10)
    password : str = Field(..., min_length=8, max_length=10)

#
class UserRead(BaseModel):
    id : int
    username : str

    model_config = ConfigDict(from_attributes=True)