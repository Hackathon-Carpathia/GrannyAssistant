from src.infrastructure.llm_communication_service import LLMCommunicationService

dependencies = {}

def initialize_dependecies():
    global dependencies
    _service = LLMCommunicationService()
    dependencies[LLMCommunicationService] = _service


def get_llm_communication_service():
    return dependencies[LLMCommunicationService]