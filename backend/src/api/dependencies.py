from src.infrastructure.communication_service import CommunicationService, CommunicationServiceConfig
# from src.infrastructure.event_handler import EventHandler, EventHandlerConfig
import os


dependencies = {}

def initialize_dependecies():
    global dependencies
    _communication_service = CommunicationService(
        config=CommunicationServiceConfig(llm_agent_url=os.getenv("LLM_AGENT_URL"),
        llm_url=os.getenv("LLM_URL"),
        event_scheduler_url=os.getenv("EVENT_SCHEDULER_URL"))
    )
    # _event_handler = EventHandler(
    #     config=EventHandlerConfig(event_scheduler_url=os.getenv("EVENT_SCHEDULER_URL"))
    # )
    dependencies[CommunicationService] = _communication_service
    # dependencies[EventHandler] = _event_handler


def get_communication_service():
    return dependencies[CommunicationService]

# def get_event_handler():
#     return dependencies[EventHandler]