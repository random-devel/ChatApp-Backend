from fastapi import APIRouter, Depends
from Authentication.AuthProcess import AuthAdmin
from .AdminServices import UpdateUsersRole, fetchUsers, BlockUsers, checkUSER
from .ValidationModels import BlockUser, UpdateRole

Admin = APIRouter(dependencies=[Depends(AuthAdmin),Depends(checkUSER)])

@Admin.get('/dashboard')
async def dashboard():
    count = await fetchUsers()
    return count

@Admin.put('/ChangeUsersRole')
async def updateRole(Schema: UpdateRole):
    await UpdateUsersRole(Schema)

@Admin.post('/BlockUser')
async def block(Schema: BlockUser):
    await BlockUsers(Schema)
