from fastapi import APIRouter, Depends
from src.api.dependencies import get_llm_communication_service
from src.infrastructure.llm_communication_service import LLMCommunicationService
from pydantic import BaseModel

router = APIRouter()

class UserQuery(BaseModel):
    question: str


@router.post("/user_request", status_code=200)
async def read_items(query: UserQuery, service: LLMCommunicationService = Depends(get_llm_communication_service)):
    ans = service.get_answer(query.question)
    pass