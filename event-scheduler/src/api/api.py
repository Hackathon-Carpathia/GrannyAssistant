from fastapi import APIRouter, Depends, BackgroundTasks

from pydantic import BaseModel
from src.domain.event import UserQuery, RegisterEvent, Event
from src.api.dependencies import get_event_service
from src.infrastructure.event_service import EventService

router = APIRouter()


@router.post("/register_event", status_code=200)
async def register_event(event: RegisterEvent, service: EventService = Depends(get_event_service)):
    await service.register_event(event)
    pass

@router.post("/trigger_event_execution", status_code=200)
async def execute_events(background_tasks: BackgroundTasks, service: EventService = Depends(get_event_service)):
    await service.execute_events(background_tasks)
    pass