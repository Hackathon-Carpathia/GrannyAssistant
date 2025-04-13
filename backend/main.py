import uvicorn
from fastapi import FastAPI
from src.api.dependencies import initialize_dependecies, get_communication_service
from src.api.api import router
from src.api.middleware import AuthMiddleware
from dotenv import load_dotenv
import asyncio
import websockets

load_dotenv(override=True)

async def create_app():
    initialize_dependecies()
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    app.add_middleware(AuthMiddleware)
    return app


async def websocket_handler(websocket, path):
    if path[:4] != '/ws/':
        await websocket.close()
        return
    id_ = int(path[4:])
    communication_service = get_communication_service()
    communication_service.add_websocket(websocket, id_)


async def start_websocket_server():
    return await websockets.serve(websocket_handler, "0.0.0.0", 42779)

async def start_fastapi_server():
    app = await create_app()
    config = uvicorn.Config(app, host="0.0.0.0", port=8001, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(
        start_websocket_server(),
        start_fastapi_server()
    )


if __name__ == "__main__":
    
    asyncio.run(main())


# async def start_websocket_server():
#     return await websockets.serve(handler, "0.0.0.0", PORT_WS)

# async def start_fastapi_server():
#     config = uvicorn.Config(app, host="0.0.0.0", port=PORT_API, log_level="info")
#     server = uvicorn.Server(config)
#     await server.serve()
