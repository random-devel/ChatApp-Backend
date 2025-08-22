from pydantic import BaseModel, EmailStr, Field
from typing import NamedTuple

class NewUser(BaseModel):
    username: str = Field(min_length=6,max_length=16)
    password: str = Field(min_length=8,max_length=20)
    email: EmailStr

class User(BaseModel):
    username: str
    password: str
