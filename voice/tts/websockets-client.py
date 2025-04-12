import asyncio
import websockets

URI = "wss://halina.wmlynik.ovh/ws"

async def listen():
    async with websockets.connect(URI) as websocket:
        print(f"Connected to {URI}")
        while True:
            try:
                message = await websocket.recv()
                print(f"Received: {message}")
            except websockets.ConnectionClosed:
                print("Connection closed.")
                break

asyncio.run(listen())
