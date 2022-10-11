import asyncio
from asyncio import Queue
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


async def broadcast_worker(queue, active_connections):
    while True:
        message = await queue.get()
        for websocket in active_connections:
            asyncio.create_task(send(websocket, message))
        queue.task_done()


class WebSocketConnectionManager:
    _instance = None

    queue = None
    active_connections: Set[WebSocket] = None

    def __new__(cls):
        if cls._instance is None:
            # Singleton Pattern: Create instance only once
            cls._instance = super(WebSocketConnectionManager, cls).__new__(cls)

            # Initiate an async queue which will contain all the messages
            # to-be-sent via websockets
            loop = asyncio.get_running_loop()
            cls.queue = Queue(loop=loop)

            # List of all active websocket clients
            cls.active_connections = set()

            # Create a background task which checks the queue for new messages
            # and broadcasts them to all active websocket clients
            asyncio.create_task(name='broadcast',
                                coro=broadcast_worker(
                                    cls.queue,
                                    cls.active_connections))

        return cls._instance

    def add_to_queue(self, message: bytes):
        if len(self.active_connections) > 0:
            self.queue.put_nowait(message)

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
