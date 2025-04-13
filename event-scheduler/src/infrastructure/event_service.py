from dataclasses import dataclass
import requests
from src.domain.event import UserQuery, RegisterEvent, Event
from src.infrastructure.event_repository import RegisterEventRepository
from fastapi import BackgroundTasks
import asyncio

@dataclass
class EventService:
    event_repository: RegisterEventRepository


    async def register_event(self, event: RegisterEvent):
        await self.event_repository.create(event)

        
    async def execute_events(self, background_tasks: BackgroundTasks):
        events = await self.event_repository.read_events_to_execute()
        for event in events:
            background_tasks.add_task(self._call_external_service, event)

    async def _call_external_service(self, event: Event):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "http://external-service/api/process",
                    json=event.dict()
                )
                response.raise_for_status()
                print(f"Event sent for user {event.user_id}")
            except httpx.HTTPError as e:
                print(f"Error for user {event.user_id}: {e}")