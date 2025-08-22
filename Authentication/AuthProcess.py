from .UserModel import User, NewUser
from fastapi import HTTPException, Request, Response
from passlib.hash import argon2
from .MakeSessions import (
        CreateUserSession,
        CreateSessions,
    )
from .MongoODM import (
        UserCred,
        UserInfo,
        Sessions,
        AdminSessions
    )
from pymongo.errors import DuplicateKeyError
from Authentication.DuplicatedOpreations import fetch,insertHandler,updateHandler,delHandler
from fastapi import Request

async def LoginUser(data: User, response: Response, request: Request):
    """Handles user login and creates session cookies."""
    if await AuthSessions(request):
        raise HTTPException(302,detail='continue to profile')

    user_dict = await fetch(UserCred,username=data.username)
    if user_dict:
        if not argon2.verify(data.password, user_dict.get('hashed_password')):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user_info = await fetch(UserInfo,username=data.username)
        if user_info:
            await CreateUserSession(Sessions,data.username,'sessionId',response,request)
            await CreateSessions(user_info,response,30,'userInfo',False)
            if user_dict.get("role") == "admin":
                await CreateUserSession(AdminSessions,data.username,'AdminSession',response,request)
        else:
            raise HTTPException(406)
    else:
        raise HTTPException(404,detail='user not found!!')

async def RegisterUser(data: NewUser, response: Response,request: Request):
    """Registers a new user and creates initial session cookies."""
    if await AuthSessions(request):
        raise HTTPException(302,detail='continue to profile')

    existing_user = await fetch(UserCred,username=data.username)
    if not existing_user:
        try:
            hashed_pass = argon2.hash(data.password)

            await insertHandler(
                UserCred,
                returnData=False,
                username=data.username,
                hashed_password=hashed_pass,
                email=data.email,
                role='user'
            )

            userInfo = await insertHandler(
                UserInfo,
                returnData=True,
                username=data.username,
                email=data.email,
                operationlevel='beginner',
            )

            if userInfo:
                await CreateUserSession(Sessions,data.username,'sessionId',response, request)
                await CreateSessions(userInfo,response,30,'userInfo',False)
            else:
                raise HTTPException(500,detail='unkown error ocured')
            
        except DuplicateKeyError:
            raise HTTPException(403,detail='email is already in use')
        except Exception as e:
            raise HTTPException(status_code=501, detail="Registration failed") from e
    else:
        raise HTTPException(302,detail='the already exists')
    
async def LogoutUser(request: Request, response: Response):
    """Invalidates user and admin sessions (logout)."""

    if adminSession:= request.cookies.get('AdminSession'):
        if authAdmin:= await fetch(AdminSessions,ID=adminSession):
            await delHandler(AdminSessions,ID=adminSession)
            response.delete_cookie("AdminSession", path="/")
    
    if Session:= request.cookies.get('sessionId'):
        if authSession:= await fetch(Sessions,ID=Session):
            await delHandler(Sessions,ID=Session)
            response.delete_cookie("sessionId", path="/")
        else:
            raise HTTPException(403,detail='conflict data')
    else:
        raise HTTPException(status_code=403, detail="No user session found")
    
async def AuthSessions(request: Request) -> bool:
    """Verifies active sessions and returns session data, if any.""" 
    session = request.cookies.get('sessionId')
    if sessionid:= await fetch(Sessions,ID=session):
        return True
    else:
        return False

async def AuthAdmin(request:Request) -> bool:
    session = request.cookies.get('AdminSession')
    if session:= await fetch(AdminSessions,ID=session):
        return True
    else:
        raise HTTPException(401)
