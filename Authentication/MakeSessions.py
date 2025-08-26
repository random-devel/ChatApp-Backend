from jose import jwt, JWTError
from fastapi import Response, Request, HTTPException
from secrets import token_urlsafe
from datetime import datetime, timedelta
from typing import Optional,Type
from beanie import Document
from .settings import settings
from .DuplicatedOpreations import insertHandler

from fastapi import Request

def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host # type: ignore
    return ip

async def CreateUserSession(
        model: Type[Document],
        username: str ,
        key: str,
        response: Response,
        request: Request
    ):
    """Creates a user session cookie with a 30-minute expiry."""
    ID= token_urlsafe(50)
    ip = get_client_ip(request)
    expire = datetime.utcnow() + timedelta(minutes=30)
    await insertHandler(
        model,
        False,
        username = username,
        IP=ip,
        ID=ID,
        expireAt=expire
    )
    response.set_cookie(
        key,
        value=ID,
        samesite='none',
        httponly=True,
        max_age=1800,
        secure=True,
        path='/'
    )

async def CreateSessions(data: dict, response: Response, expiresMinutes: int, key: str, returned: Optional[bool]) -> str | None:
    """Creates a custom session cookie with a set expiry and key.,, jwt only!!"""
    data.update({"exp": datetime.utcnow() + timedelta(minutes=expiresMinutes)})
    try:
        payload = jwt.encode(data, settings.secret_key, settings.algorithm)
        response.set_cookie(
            key,
            value=payload,
            max_age=expiresMinutes * 60,
            samesite='none',
            httponly=True,
            secure=True,
            path='/'
        )
        if returned is not None:
            return payload
    except JWTError as e:
        raise HTTPException(status_code=501, detail="Session creation failed") from e

async def checkBlockedSessions(request: Request, items: list):
    """Ensures that none of the blocked cookies are present in the request."""
    for cookie in items:
        if request.cookies.get(cookie):
            raise HTTPException(status_code=401, detail="Not allowed: finish logout or reset password process")

