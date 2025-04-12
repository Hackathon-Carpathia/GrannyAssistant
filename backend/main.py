import uvicorn
from fastapi import FastAPI
from src.api.dependencies import initialize_dependecies, get_llm_communication_service
from src.api.api import router


def create_app():
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    return app

if __name__ == "__main__":
    initialize_dependecies()
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)