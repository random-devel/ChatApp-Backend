from Authentication.AuthProcess import AuthSessions
from fastapi import Request, HTTPException,WebSocket, WebSocketDisconnect
from .ConnectionManager import ConnectionManaget
from Authentication.DuplicatedOpreations import fetch
from Authentication.MongoODM import Sessions

connManager = ConnectionManaget()

async def AuthUser(request: Request):
    if await AuthSessions(request):
        return True
    else:
        raise HTTPException(401,detail='you need to login to attemp the request')
    
async def Manager(socket: WebSocket):
    await connManager.connect(socket)

    session = socket.cookies.get('sessionId')

    if data:= await fetch(Sessions,ID=session):
        username = data.get('username')
    else:
        await socket.close(code=4003)

    try:
        while True:
            content = await socket.receive_json()
            await connManager.sendMessage(f"User {username}: {content}")
    except WebSocketDisconnect:
        connManager.disconnect(socket)


async def loadContent():
    pass