from dataclasses import dataclass
import requests
from src.domain.event import UserQuery, Event, RegisterEvent

@dataclass
class CommunicationServiceConfig:
    llm_agent_url: str  
    llm_url: str
    event_scheduler_url: str    

@dataclass
class CommunicationService:
    config: CommunicationServiceConfig

    def get_answer_from_llm_agent(self, query: UserQuery) -> str:
        return self._post(
            url=self.config.llm_agent_url,
            data=query.dict()
        )

    def execute_event(self, event: Event):
        return self._post(
            url=self.config.llm_url,
            data=event.dict()
        )

    def register_event(self, event: RegisterEvent):
        return self._post(
            url=self.config.event_scheduler_url,
            data=event.dict()
        )

    def _post(self, url: str, data: dict):
        print(data)
        return
        try:
            response = requests.post(
                url,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json() 
        except requests.RequestException as e:
            print(f"Request to {url} failed:", e)
            return f"Error: {e}"