from pydantic import BaseModel, Field

class resetAuth(BaseModel):
    username: str

class OTP(BaseModel):
    otp: str

class resetPasswd(BaseModel):
    password: str = Field(min_length=10, max_length=20)