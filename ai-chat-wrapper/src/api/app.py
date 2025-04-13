from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.infrastructure.model import send_message
from src.api.metadata.response import UserRequest
import requests
router = APIRouter()

@router.post("/ask", status_code=200)
async def talk_with_user(query: UserRequest):
    response = send_message(f'"{query.req_type}+prompt":{query.prompt}')
    print(response)
    return response
    
    
    

