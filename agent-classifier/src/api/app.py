from src.infrastructure.llama import generate_response, parse_response
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api.metadata.response import UserRequest, LLMResponse, SMSMetadata, ChatRequest
import requests
router = APIRouter()
def send_sms(sms_metadata: SMSMetadata):
    url = "http://0.0.0.0:8777/api/v1/twilio/sendSMS"
    # Wysłanie POST z danymi
    response = requests.post(
        url,
        json=sms_metadata.model_dump()  # Zamieniamy obiekt Pydantic na słownik
    )

    # Sprawdzanie odpowiedzi
    if response.status_code == 200:
        print("SMS wysłany pomyślnie!")
    else:
        print(f"Błąd: {response.status_code} - {response.text}")


def ask_llm(chat_request: ChatRequest):
    url = "http://0.0.0.0:42781/api/v1/ai-chat/ask/"
    response = requests.post(
    url,
    json=chat_request.model_dump()  # Zamieniamy obiekt Pydantic na słownik
    )
    if response.status_code == 200:
        print("Wyslano pomyslnie")
        return response

@router.post("/user_request", status_code=200)
async def get_answer_from_llm_agent(query: UserRequest):
    response = generate_response(generate_response(query.prompt))
    ocena_sytuacji, powod_decyzji = parse_response(response)
    if ocena_sytuacji.lower() == "emergency":
        sms_metadata = SMSMetadata(to_number="+48735406396", message=powod_decyzji)
        send_sms(sms_metadata)
        return
    else:
        chat_request = ChatRequest(req_type="user", user_id="1", prompt=query.prompt)
        ans = ask_llm(chat_request=chat_request)
        print(ans.json())
        return ans.json()
