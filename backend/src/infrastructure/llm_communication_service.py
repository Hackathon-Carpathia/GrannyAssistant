from dataclasses import dataclass
import requests
from src.domain.event import UserQuery

@dataclass
class LLMCommunicationServiceConfig:
    llm_agent_url: str  

@dataclass
class LLMCommunicationService:
    config: LLMCommunicationServiceConfig

    def get_answer_from_llm_agent(self, query: UserQuery) -> str:
        try:
            response = requests.post(
                self.config.llm_agent_url,
                json=query.dict(),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("answer", "No answer")
        except requests.RequestException as e:
            return f"Error, no answer from llm: {e}"