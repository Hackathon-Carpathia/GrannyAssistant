import uvicorn
import asyncio
from fastapi import FastAPI
from src.api.dependencies import initialize_dependecies, get_event_repository
from src.api.api import router
from dotenv import load_dotenv

load_dotenv(override=True)

async def create_app():
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    db_connector = get_event_repository()
    await db_connector.connector.create_all()
    return app

if __name__ == "__main__":
    initialize_dependecies()
    app = asyncio.run(create_app())
    uvicorn.run(app, host="0.0.0.0", port=8000)