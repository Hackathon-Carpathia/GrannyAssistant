from src.infrastructure.communication_service import CommunicationService, CommunicationServiceConfig
import os


dependencies = {}

def initialize_dependecies():
    global dependencies
    _communication_service = CommunicationService(
        config=CommunicationServiceConfig(llm_agent_url=os.getenv("LLM_AGENT_URL"),
        llm_url=os.getenv("LLM_URL"),
        event_scheduler_url=os.getenv("EVENT_SCHEDULER_URL"))
    )

    dependencies[CommunicationService] = _communication_service


def get_communication_service():
    return dependencies[CommunicationService]
