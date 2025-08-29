from pydantic import BaseModel, Field, EmailStr

class resetAuth(BaseModel):
    username: str

class OTP(BaseModel):
    otp: str

class resetPasswd(BaseModel):
    password: str = Field(min_length=10, max_length=20)

class SendMails(BaseModel):
    OTP: str
    TargetMail: EmailStr

class INSERTotp(BaseModel):
    username: str
    email: EmailStr

class VerifyOTP(BaseModel):
    username: str
    otp: str