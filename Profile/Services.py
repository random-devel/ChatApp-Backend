from fastapi import Request , Response, HTTPException
from Authentication.settings import settings
from jose import jwt , JWTError
from Authentication.AuthProcess import AuthSessions

async def checkUser(request: Request):
    if await AuthSessions(request):
        return True
    raise HTTPException(401)

async def verifyCookieKey(key: str, request: Request) -> dict | None:
    """Verifies a cookie by decoding its JWT and optionally checking if it's blocked."""
    data = request.cookies.get(key)
    if data:
        try:
            payload = jwt.decode(data, settings.secret_key, settings.algorithm)
            data = payload.copy()
            del data['exp']
            return data
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Invalid session") from e
    raise HTTPException(401)

async def profile(request: Request):
    return await verifyCookieKey('userInfo',request)

async def getUsersProfile(username):
    pass
