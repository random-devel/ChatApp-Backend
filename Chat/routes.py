from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from .ConnectionManager import ConnectionManaget
from .Services import AuthUser, Manager

chat = APIRouter(prefix='/chat')

socketMange = ConnectionManaget()

@chat.get('/auth')
async def authenticated(auth = Depends(AuthUser)):
    return {'hello'}

@chat.get('/load')
async def load(auth = Depends(AuthUser)):
    return {'status': 'success'}

@chat.websocket('/global')
async def main(socket : WebSocket):
    await Manager(socket)