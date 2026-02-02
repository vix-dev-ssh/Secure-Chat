
import asyncio
from fastapi import FastAPI, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from src.manager import manager  # Import the manager we just made

app = FastAPI(title="Secure Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"message": "OK"}

# --- NEW WEBSOCKET CODE ---
@app.websocket("/ws/{room_id}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_name: str):
    await manager.connect(websocket, room_id)
    try:
        # Start a background task to listen to Redis
        consumer_task = asyncio.create_task(manager.consume(websocket, room_id))
        
        while True:
            # Wait for user to type something
            data = await websocket.receive_text()
            # Broadcast it to everyone in the room
            await manager.broadcast(room_id, f"{user_name}: {data}")
            
    except WebSocketDisconnect:
        # Handle disconnect (optional: cleanup)
        pass