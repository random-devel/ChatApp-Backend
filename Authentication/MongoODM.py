from beanie import Document,Indexed
from pydantic import BaseModel,IPvAnyAddress,EmailStr,Field
from datetime import datetime
from typing import Annotated
from pymongo import IndexModel

class UserCred(Document):
    username: Annotated[str,Indexed(unique=True)]
    email: Annotated[EmailStr,Indexed(unique=True)] 
    hashed_password: str
    role: str

    class Settings:
        name = "users"

class UserInfo(Document):
    username: Annotated[str,Indexed(unique=True)]
    email: Annotated[EmailStr,Indexed(unique=True)] 
    operationlevel: str

    class Settings:
        name = "userInfo"

class OTPdocuments(Document):
    username: str
    hashedOTP: str
    expireAt: datetime

    class Settings:
        name= "OTPdocs"
        indexes = [
            IndexModel(  
                [("expireAt", 1)],  
                expireAfterSeconds=0
            )
        ]


class TempStage1(Document):
    username: Annotated[str,Indexed(unique=True)]
    session: str
    expireAt: datetime


    class Settings:
        name = "stage1"
        indexes = [
            IndexModel(  
                [("expireAt", 1)],  
                expireAfterSeconds=0
            )
        ]

class TempStage2(Document):
    username: Annotated[str,Indexed(unique=True)]
    session: str
    expireAt: datetime

    class Settings:
        name = "stage2"
        indexes = [
            IndexModel(  
                [("expireAt", 1)],  
                expireAfterSeconds=0
            )
        ]

class BlockedResetPasswd(Document):
    username: Annotated[str,Indexed(unique=True)]
    expireAt: datetime

    class Settings:
        name="BlockedReset"
        indexes = [
            IndexModel(  
                [("expireAt", 1)],  
                expireAfterSeconds=0
            )
        ]

class BlockedUsers(Document):
    username: Annotated[str,Indexed(unique=True)]
    reason: str = Field(min_length=30,max_length=250)
    blockedAt: datetime
    expireAt:datetime

    class Settings:
        name="BlockedUsers"
        indexes = [
            IndexModel(  
                [("expireAt", 1)],  
                expireAfterSeconds=0
            )
        ]

class Sessions(Document):
    username: str
    IP: IPvAnyAddress
    ID: Annotated[str,Indexed(unique=True)]
    expireAt: datetime

    class Settings:
        name="Sessions"
        indexes = [
            IndexModel(  
                [("expireAt", 1)],  
                expireAfterSeconds=0
            )
        ]

class AdminSessions(Document):
    username: Annotated[str,Indexed(unique=True)]
    IP: IPvAnyAddress
    ID: Annotated[str,Indexed(unique=True)]
    expireAt: datetime

    class Settings:
        name="AdminSessions"
        indexes = [
            IndexModel(  
                [("expireAt", 1)],  
                expireAfterSeconds=0
            )
        ]

class globalMessages(Document):
    username: str
    content: str
    sendAt: datetime

    class Settings:
        name="globalMessages"

