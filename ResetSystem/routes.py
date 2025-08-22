from fastapi import APIRouter, Request, Response
from .Services import AuthResetPassword,AuthOTP,ResetPasswd
from .Models import resetAuth, OTP, resetPasswd

AuthReset= APIRouter(prefix='/reset')

@AuthReset.post("/Auth")
async def userReset(data: resetAuth, response: Response, request: Request):
    """Send OTP for password reset."""
    await AuthResetPassword(data.username, response, request)
    return {"message": "OTP sent for password reset"}

@AuthReset.post("/checkOTP")
async def checkOTP(OTP: OTP, request: Request, response: Response):
    """Verify OTP for password reset."""
    await AuthOTP(OTP.otp, request, response)
    return {"message": "OTP verified, proceed with password reset"}

@AuthReset.put("/NewPasswd")
async def reset(newPassword: resetPasswd, request: Request, response: Response):
    """Reset user password."""
    await ResetPasswd(newPassword.password, request, response)
    return {'success':"continue to the login"}