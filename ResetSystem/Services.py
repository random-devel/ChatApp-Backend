from fastapi import HTTPException, Request, Response
from passlib.hash import argon2
from .OTPverify import insertOTP, verifyOTP
from Authentication.MakeSessions import checkBlockedSessions
from Authentication.MongoODM import UserCred, TempStage1, TempStage2, OTPdocuments
from Authentication.DuplicatedOpreations import fetch,delHandler,updateHandler
from .MakeStages import createStageSession, VerifyStageSession
from .Models import INSERTotp, VerifyOTP

async def AuthResetPassword(username: str, response: Response, request: Request):
    """
    Initiates password reset by sending an OTP and creating a stage1 session.
    """
    blocked_list = ["stage1", "sessionId", "stage2", "AdminSession"]
    await checkBlockedSessions(request, blocked_list)
    if user:= await fetch(UserCred,username=username):
        if OTP:= await fetch(OTPdocuments,username=username):
            raise HTTPException(401,detail='complete the reset password proccess')

        await insertOTP(INSERTotp(username=username, email=user.get('email')))  # type: ignore

        await createStageSession(TempStage1,'stage1',username,response)
    else:
        raise HTTPException(404)

async def AuthOTP(OTP: str, request: Request, response: Response):
    """Verifies the OTP and creates a stage2 session."""

    await checkBlockedSessions(request, ["sessionId", "stage2", "AdminSession"])

    if StageData:= await VerifyStageSession(TempStage1,'stage1',request):
        await verifyOTP(VerifyOTP(username=StageData.get('username'), otp=OTP)) # type: ignore
        await createStageSession(TempStage2,'stage2',StageData.get('username'),response) # type: ignore
        await delHandler(TempStage1,username=StageData.get('username'))
        response.delete_cookie('stage1')
    else:
        raise HTTPException(403,detail='bad data signatures')


async def ResetPasswd(newpassword: str, request: Request, response: Response):
    """
    Completes password reset by updating the user's password and invalidating temporary sessions.
    """
    await checkBlockedSessions(request, ["AdminSession", "sessionId",'stage1'])

    if stageData:= await VerifyStageSession(TempStage2,'stage2',request):
        newpasswd = argon2.hash(newpassword)
        await updateHandler(UserCred,{'username':stageData.get('username')},hashed_password=newpasswd)
        await delHandler(TempStage2,username=stageData.get('username'))
        response.delete_cookie('stage2')
    else:
        raise HTTPException(401, detail='session is missing')
