from fastapi import APIRouter, Depends

from pydantic import BaseModel
from src.domain.event import UserQuery, RegisterEvent, Event
from src.api.dependencies import get_event_service
from src.infrastructure.event_service import EventService

router = APIRouter()



@router.post("/register_event", status_code=200)
def register_event(event: RegisterEvent, service: EventService = Depends(get_event_service)):
    service.register_event(event)
    pass

