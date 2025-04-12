from fastapi import APIRouter, Depends
from src.api.dependencies import get_llm_communication_service, get_event_handler
from src.infrastructure.llm_communication_service import LLMCommunicationService
from pydantic import BaseModel
from src.domain.event import UserQuery, RegisterEvent, Event
from src.infrastructure.event_handler import EventHandler

router = APIRouter()


@router.post("/user_request", status_code=200)
async def get_answer_from_llm_agent(query: UserQuery, service: LLMCommunicationService = Depends(get_llm_communication_service)):
    ans = service.get_answer_from_llm_agent(query)
    pass


@router.post("/register_event", status_code=200)
def register_event(event: RegisterEvent, service: EventHandler = Depends(get_event_handler)):
    service.register_event(event)
    pass

@router.post("/call_event", status_code=200)
def register_event(event: Event, service: EventHandler = Depends(get_event_handler)):
    service.execute_event(event)
    pass
