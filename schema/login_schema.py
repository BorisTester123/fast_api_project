from pydantic import BaseModel, Field

class LoginSchema(BaseModel):
    username: str = Field(...,examples=["login"])
    password: str = Field(...,examples=["password"])
