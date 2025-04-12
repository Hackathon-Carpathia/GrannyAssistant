from src.infrastructure.llm_communication_service import LLMCommunicationService, LLMCommunicationServiceConfig
from src.infrastructure.event_handler import EventHandler, EventHandlerConfig
import os


dependencies = {}

def initialize_dependecies():
    global dependencies
    _llm_communication_service = LLMCommunicationService(
        config=LLMCommunicationServiceConfig(llm_agent_url=os.getenv("LLM_AGENT_URL"))
    )
    _event_handler = EventHandler(
        config=EventHandlerConfig(event_scheduler_url=os.getenv("EVENT_SCHEDULER_URL"))
    )
    dependencies[LLMCommunicationService] = _llm_communication_service
    dependencies[EventHandler] = _event_handler


def get_llm_communication_service():
    return dependencies[LLMCommunicationService]

def get_event_handler():
    return dependencies[EventHandler]