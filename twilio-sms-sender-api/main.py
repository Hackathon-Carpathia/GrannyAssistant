import uvicorn
from fastapi import FastAPI
from src.twilio_api_sender import router
from dotenv import load_dotenv

load_dotenv(override=True)

def create_app():
    app = FastAPI()
    app.include_router(router, prefix="/api/v1/twilio")
    return app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8777)