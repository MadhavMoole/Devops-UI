from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.websocket_manager import manager
from app.api.v1.dependencies import get_current_user

router = APIRouter()

@router.websocket("/ws/deployments/{deployment_id}")
async def deployment_status_websocket(
    websocket: WebSocket, 
    deployment_id: int
):
    # Note: WebSocket authentication is handled differently than HTTP.
    # In production, we would extract the token from the query string or a sub-protocol.
    await manager.connect(websocket, deployment_id)
    try:
        while True:
            # Keep connection alive and listen for any client messages
            data = await websocket.receive_text()
            # We can handle client-side heartbeats here
    except WebSocketDisconnect:
        manager.disconnect(websocket, deployment_id)
