from pydantic import BaseModel, ConfigDict

class UserRequestCreate(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    hashed_password: str

class User(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
