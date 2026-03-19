from pydantic import BaseModel, ConfigDict

class SBook(BaseModel):
    id: int
    name: str
    author: str | None = None
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)

class SBookAdd(BaseModel):
    name: str
    author: str | None = None
    description: str | None = None

class ErrorResponse(BaseModel):
    name: str