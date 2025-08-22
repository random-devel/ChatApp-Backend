from fastapi import APIRouter, Depends
from Authentication.AuthProcess import AuthAdmin
from .AdminServices import UpdateUsersRole, DeleteUsers, fetchUsers, BlockUsers, checkUSER

Admin = APIRouter(dependencies=[Depends(AuthAdmin),Depends(checkUSER)])

@Admin.get('/dashboard')
async def dashboard():
    count = await fetchUsers()
    return count

@Admin.put('/ChangeUsersRole')
async def updateRole(username:str,role: str):
    await UpdateUsersRole(username,role)
    
@Admin.delete('/DeleteUser')
async def delUser(username: str):
    await DeleteUsers(username)

@Admin.post('/BlockUser')
async def block(username: str,days:int,reason:str):
    await BlockUsers(username,reason,days)
