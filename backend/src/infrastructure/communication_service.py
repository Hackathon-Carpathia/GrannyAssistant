from dataclasses import dataclass, field
import requests
from src.domain.event import UserQuery, Event, RegisterEvent, LLMResponse
import json
from typing import Dict
from fastapi import WebSocket
import httpx


@dataclass
class CommunicationServiceConfig:
    llm_agent_url: str  
    llm_url: str
    event_scheduler_url: str    

@dataclass
class CommunicationService:
    config: CommunicationServiceConfig
    connected_clients: Dict[int, WebSocket] = field(default_factory=dict)

    async def get_answer_from_llm_agent(self, query: UserQuery) -> str:
        response = await self._post(
            url=self.config.llm_agent_url,
            data=query.to_dict()
        )
        print(response)
        # message = response.get('message')
        await self.broadcast_messages(response, query.user_id)

    async def execute_event(self, event: Event):
        response = await self._post(
            url=self.config.llm_url,
            data=event.to_dict()
        )
        response = response.json()
        message = response.get('message')
        await self.broadcast_messages(message, event.user_id)

    async def register_event(self, event: RegisterEvent):
        await self._post(
            url=self.config.event_scheduler_url,
            data=event.to_dict()
        )

    async def _post(self, url: str, data: dict):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=data,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                print(f"Request to {url} failed: {e}")
                return f"Error: {e}"

    async def add_websocket(self, websocket, id_: int):
        self.connected_clients[id_] = websocket

    async def broadcast_messages(self, message: str, id_: int):
        ws = self.connected_clients[id_]

        try:
            await ws.send(message)
        except:
            self.connected_clients.pop(id_, None)
