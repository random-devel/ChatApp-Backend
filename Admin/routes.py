from fastapi import APIRouter, Depends
from Authentication.AuthProcess import AuthAdmin
from .AdminServices import UpdateUsersRole, fetchUsers, BlockUsers, checkUSER
from .ValidationModels import BlockUser, UpdateRoleSchema

Admin = APIRouter(dependencies=[Depends(AuthAdmin),Depends(checkUSER)], prefix='/Admin')

@Admin.get('/check')
async def check():
    return {"status": "Admin route is working"}

@Admin.get('/dashboard')
async def dashboard():
    count = await fetchUsers()
    return count

@Admin.put('/ChangeUsersRole')
async def updateRole(Schema: UpdateRoleSchema):
    await UpdateUsersRole(Schema)

@Admin.post('/BlockUser')
async def block(Schema: BlockUser):
    await BlockUsers(Schema)
