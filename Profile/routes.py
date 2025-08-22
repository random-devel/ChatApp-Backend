from fastapi import APIRouter,Depends,Request,Response
from .Services import profile, checkUser

Profile = APIRouter(prefix='/profile', dependencies=[Depends(checkUser)])

@Profile.get('/home')
async def home(request: Request):
    return await profile(request)
