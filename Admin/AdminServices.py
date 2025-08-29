from fastapi import HTTPException,Request
from Authentication.MongoODM import BlockedUsers,UserInfo,UserCred,Sessions
from datetime import datetime, timedelta
from Authentication.AuthProcess import AuthSessions
from Authentication.DuplicatedOpreations import fetch, updateHandler, insertHandler, delHandler
from .ValidationModels import UpdateRoleSchema, BlockUser
from beanie.exceptions import DocumentNotFound, WrongDocumentUpdateStrategy, DocumentWasNotSaved
from pymongo.errors import DuplicateKeyError

async def checkUSER(request: Request):
    if await AuthSessions(request):
        return True
    else:
        raise HTTPException(401,detail='missing sessions found')

async def fetchUsers():
    count = await UserInfo.find_all().count()
    return count

async def UpdateUsersRole(updateRole: UpdateRoleSchema):
    try:
        await updateHandler(UserCred,{'username':updateRole.username},role=updateRole.role)
    except DocumentNotFound:
        raise HTTPException(404,detail='the document was not even found')
    except WrongDocumentUpdateStrategy:
        raise HTTPException(500,detail='wrong update strategy')
    except DocumentWasNotSaved:
        raise HTTPException(502,detail='failed to save the document , check the db connection')

async def BlockUsers(blockedSchema: BlockUser):
    if user:= fetch(UserCred,username=blockedSchema.username):
        try:
            await insertHandler(
                BlockedUsers,
                False,
                username=blockedSchema.username,
                reason=blockedSchema.reason,
                blockedAt=datetime.utcnow(),
                expireAt=datetime.utcnow() + timedelta(days=blockedSchema.expireAtDays)
            )

            await delHandler(Sessions,username=blockedSchema.username)
            
        except DocumentWasNotSaved:
            raise HTTPException(500,detail='document was not saved , check the db for more information')
        except DuplicateKeyError:
            raise HTTPException(403,detail='document already created')
    else:
        raise HTTPException(404, detail='the user not found')
