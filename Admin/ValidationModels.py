from pydantic import BaseModel, Field

class BlockUser(BaseModel):
    username: str
    reason: str = Field(min_length=20,max_length=250)
    expireAtDays: int

class UpdateRole(BaseModel):
    username: str
    role: str