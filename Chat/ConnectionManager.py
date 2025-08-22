from fastapi import WebSocket

class ConnectionManaget:
    def __init__(self):
        self.activeConnections: set[ WebSocket] = set()
    
    async def connect(self,websocket: WebSocket):
        await websocket.accept()
        self.activeConnections.add(websocket)
    
    def disconnect(self,websocket: WebSocket):
        self.activeConnections.discard(websocket)
    
    async def sendMessage(self,message: str):
        for connection in self.activeConnections:
            await connection.send_json({"message": message})
