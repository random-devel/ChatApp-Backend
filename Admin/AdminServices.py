from fastapi import HTTPException,Request
from passlib.hash import argon2
from typing import Optional
from Authentication.MongoODM import BlockedUsers,UserInfo,UserCred
from datetime import datetime, timedelta
from Authentication.AuthProcess import AuthSessions

async def checkUSER(request: Request):
    if await AuthSessions(request):
        return True
    else:
        raise HTTPException(401,detail='missing sessions found')

async def fetchUsers():
    count = await UserInfo.find_all().count()
    return count

async def UpdateUsersRole(username: str, role: str):
    user = await UserCred.find_one(UserCred.username == username)
    if user:
        user.role = role
        await user.save()
    else:
        raise HTTPException(404,detail='user not found')

async def DeleteUsers(username: str):
    user = await UserCred.find_one(UserCred.username == username)
    if user:
        await user.delete()
        await UserInfo.delete(UserInfo.username == username)
        return {'success'}
    else:
        raise HTTPException(404,detail='user not found')
        
async def BlockUsers(username: str ,reason: str ,BlockedDays: int):
    user = UserCred.find_one(UserCred.username == username)
    if user:
        blockedUser = BlockedUsers(
            username=username,
            reason=reason,
            blockedAt=datetime.utcnow(),
            expireAt=datetime.utcnow() + timedelta(days=BlockedDays)
        )
        await blockedUser.insert()
    else:
        raise HTTPException(404)
