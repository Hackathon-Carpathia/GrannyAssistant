from dataclasses import dataclass
import requests
from src.domain.event import UserQuery, RegisterEvent
from src.infrastructure.event_repository import RegisterEventRepository

# @dataclass
# class EventServiceConfig:
#     idk: str  

@dataclass
class EventService:
    event_repository: RegisterEventRepository
    # config: EventServiceConfig


    def register_event(self, event: RegisterEvent):
        self.event_repository.create(event)
        self.event_repository.read_events_to_execute()
        
    # def get_answer_from_llm_agent(self, query: UserQuery) -> str:
    #     try:
    #         response = requests.post(
    #             self.config.llm_agent_url,
    #             json=query.dict(),
    #             timeout=10
    #         )
    #         response.raise_for_status()
    #         data = response.json()
    #         return data.get("answer", "No answer")
    #     except requests.RequestException as e:
    #         return f"Error, no answer from llm: {e}"