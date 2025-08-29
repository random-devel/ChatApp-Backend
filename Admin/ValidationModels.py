from pydantic import BaseModel, Field
from typing import Literal

class BlockUser(BaseModel):
    username: str
    reason: str = Field(min_length=20,max_length=250)
    expireAtDays: int


class UpdateRoleSchema(BaseModel):
    username: str
    role: Literal["admin", "user"]