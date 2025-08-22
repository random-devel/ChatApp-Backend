from fastapi import APIRouter, Request,Depends, HTTPException
from fastapi.responses import Response
from .UserModel import User,  NewUser
from .AuthProcess import LoginUser, RegisterUser, LogoutUser, AuthSessions

auth = APIRouter(prefix='/auth')

@auth.get('/check')
async def check(authenticated: bool = Depends(AuthSessions)):
    if authenticated:
        raise HTTPException(403,detail='you are already authenticated, logout to complete the proccess')
    else:
        return {'authinticated':False}

@auth.post("/login")
async def login(credentials: User, response: Response,request: Request):
    """Login a user."""
    await LoginUser(credentials, response,request)
    return {"success": "Welcome"}

@auth.post("/register")
async def register(new_user: NewUser, response: Response,request: Request):
    """Register a new user."""
    await RegisterUser(new_user, response,request)
    return {"success": "Welcome"}

@auth.post("/logout")
async def logout(request: Request, response: Response):
    """Logout a user."""
    await LogoutUser(request, response)
    return {"message": "Logged out"}