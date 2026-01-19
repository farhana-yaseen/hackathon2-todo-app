"""
WebSocket Manager for Real-time Task Updates
"""
import json
from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
from uuid import UUID, uuid4


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}  # user_id -> list of websockets

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            # Clean up empty lists
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except WebSocketDisconnect:
                    disconnected.append(connection)

            # Remove disconnected connections
            for conn in disconnected:
                try:
                    self.active_connections[user_id].remove(conn)
                    if not self.active_connections[user_id]:
                        del self.active_connections[user_id]
                except ValueError:
                    pass  # Connection already removed

    async def broadcast_to_user(self, message: dict, user_id: str):
        await self.send_personal_message(message, user_id)


# Global instance
manager = ConnectionManager()


async def broadcast_task_update(user_id: str, change_type: str, task_data: dict = None):
    """
    Broadcast task changes to all connected websockets for a specific user
    """
    message = {
        "event": "task_update",
        "change_type": change_type,
        "task_data": task_data,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }
    await manager.broadcast_to_user(message, user_id)