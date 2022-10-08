import asyncio
from typing import Set

from fastapi import WebSocket
from loguru import logger
from starlette.websockets import WebSocketState


async def send(websocket: WebSocket, message: bytes):
    if websocket.client_state is WebSocketState.DISCONNECTED:
        return
    try:
        await websocket.send_bytes(message)
    except RuntimeError:
        pass


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def handle(self, websocket: WebSocket):
        await self.connect(websocket)
        try:
            while websocket.client_state is not WebSocketState.DISCONNECTED:
                _ = await websocket.receive()
        except RuntimeError:
            self.disconnect(websocket)

    async def connect(self, websocket: WebSocket):
        logger.debug("WebSocket client connected")
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        logger.debug("WebSocket client disconnected")
        self.active_connections.remove(websocket)

    def broadcast(self, message: bytes):
        for websocket in self.active_connections:
            asyncio.create_task(send(websocket, message))


ws_manager = WebSocketConnectionManager()
