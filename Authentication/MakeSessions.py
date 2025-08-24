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
        samesite='lax',
        httponly=True,
        max_age=1800,
        secure=False,
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
            samesite='lax',
            httponly=True,
            secure=False,
            path='/'
        )
        if returned is not None:
            return payload
    except JWTError as e:
        raise HTTPException(status_code=501, detail="Session creation failed") from e

def verifyCookieKey(key: str, request: Request) -> tuple[dict, str] | None:
    """Verifies a cookie by decoding its JWT and optionally checking if it's blocked."""
    data = request.cookies.get(key)
    if data:
        try:
            payload = jwt.decode(data, settings.secret_key, settings.algorithm)
            return payload,data
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Invalid session") from e
    return None

def checkBlockedSessions(request: Request, items: list):
    """Ensures that none of the blocked cookies are present in the request."""
    for cookie in items:
        if request.cookies.get(cookie):
            raise HTTPException(status_code=401, detail="Not allowed: finish logout or reset password process")

