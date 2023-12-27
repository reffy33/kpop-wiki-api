from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router_websocket = APIRouter()

class WebSocketManager:
    def __init__(self) -> None:
        self.connections: list[WebSocket] = []
    
    async def connect(self, wb: WebSocket):
        await wb.accept()
        self.connections.append(wb)

    def disconnect(self, wb: WebSocket):
        self.connections.remove(wb)

    
    async def send_direct_message(self, message: str, wb: WebSocket):
        await wb.send_text(message)

manager = WebSocketManager()

async def send_broadcast(message: str):
    print(f'Recieved message: {message}')
    for connection in manager.connections:
            await connection.send_text(message)
    print('Message sent')



@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(wb: WebSocket, client_id: int):
    await manager.connect(wb)
    await send_broadcast(f"Client {client_id} has joined the chat")

    try:
        while True:
            data = await wb.receive_text()
            await send_broadcast(f"#{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(wb)
        await send_broadcast(f"The client {client_id} has left the chat")