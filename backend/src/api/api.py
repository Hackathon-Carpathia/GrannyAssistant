from fastapi import APIRouter, Depends
from src.api.dependencies import get_communication_service
from src.infrastructure.communication_service import CommunicationService
from pydantic import BaseModel
from src.domain.event import UserQuery, RegisterEvent, Event
# from src.infrastructure.event_handler import EventHandler

router = APIRouter()


@router.post("/user_request", status_code=200)
async def get_answer_from_llm_agent(query: UserQuery, service: CommunicationService = Depends(get_communication_service)):
    ans = await service.get_answer_from_llm_agent(query)
    pass


@router.post("/register_event", status_code=200)
async def register_event(event: RegisterEvent, service: CommunicationService = Depends(get_communication_service)):
    print('register')
    await service.register_event(event)
    pass

@router.post("/call_event", status_code=200)
async def register_event(event: Event, service: CommunicationService = Depends(get_communication_service)):
    await service.execute_event(event)
    pass
