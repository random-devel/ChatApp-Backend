from fastapi import Response, Request, HTTPException
from secrets import token_urlsafe
from beanie import Document
from typing import Type
from Authentication.DuplicatedOpreations import insertHandler, fetch
from datetime import timedelta, datetime

async def createStageSession(model: Type[Document], key: str, username: str, response: Response):
    session = token_urlsafe(40)
    await insertHandler(
        model,
        False,
        username=username,
        session=session,
        expireAt=datetime.utcnow() + timedelta(minutes=10),
    )
    response.set_cookie(
        key,
        value=session,
        path='/',
        httponly=True,
        samesite='none',
        secure=True,
        max_age=600
    )

async def VerifyStageSession(model: Type[Document],key: str, request: Request) -> dict:
    if session:= request.cookies.get(key):
        if verify:= await fetch(model,session=session):
            return verify
        else:
            raise HTTPException(401,detail='session is invalid')
    else:
        raise HTTPException(401, detail='missing session')