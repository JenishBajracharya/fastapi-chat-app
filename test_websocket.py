import websockets
import asyncio
import json

async def test():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYW0iLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NTE4Nzk1ODl9.WDPuuNwV5ML5EVOYw09fwmYIjl_ZL6eGtW90MiTSySQ"
    uri = f"ws://127.0.0.1:8000/ws/chatroom?token={token}"
    
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"content": "Hello from Python WebSocket!"}))
        while True:
            response = await websocket.recv()
            print("Received:", response)

asyncio.run(test())
