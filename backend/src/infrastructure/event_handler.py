from dataclasses import dataclass
from src.domain.event import RegisterEvent, Event
import requests

@dataclass
class EventHandlerConfig:
    event_scheduler_url: str  

@dataclass
class EventHandler:
    config: EventHandlerConfig

    def register_event(self, event: RegisterEvent):
        try:
            response = requests.post(
                self.config.event_scheduler_url,
                json=event.dict(),
                timeout=10
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(e)
            return f"Error: {e}"

    def execute_event(self, event: Event):
        pass