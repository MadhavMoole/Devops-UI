from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import asyncio

class ConnectionManager:
    def __init__(self):
        # Maps deployment_id to a list of active WebSocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, deployment_id: int):
        await websocket.accept()
        if deployment_id not in self.active_connections:
            self.active_connections[deployment_id] = []
        self.active_connections[deployment_id].append(websocket)

    def disconnect(self, websocket: WebSocket, deployment_id: int):
        if deployment_id in self.active_connections:
            self.active_connections[deployment_id].remove(websocket)
            if not self.active_connections[deployment_id]:
                del self.active_connections[deployment_id]

    async def broadcast_to_deployment(self, deployment_id: int, message: dict):
        if deployment_id in self.active_connections:
            for connection in self.active_connections[deployment_id]:
                await connection.send_json(message)

manager = ConnectionManager()
