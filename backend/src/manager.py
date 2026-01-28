
import os
import json
import redis.asyncio as redis
from fastapi import WebSocket

class RedisManager:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis = redis.from_url(self.redis_url, decode_responses=True)
        self.pubsub = self.redis.pubsub()

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        # Subscribe to the specific room
        await self.pubsub.subscribe(room_id)
        
    async def broadcast(self, room_id: str, message: str):
        # Publish message to Redis (so all workers see it)
        await self.redis.publish(room_id, message)

    async def consume(self, websocket: WebSocket, room_id: str):
        # Listen for messages from Redis and send to the user
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])

manager = RedisManager()