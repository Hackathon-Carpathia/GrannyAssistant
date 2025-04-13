from pydantic import BaseModel


class UserRequest(BaseModel):
    user_id: str
    prompt: str

class LLMResponse(BaseModel):
    OCENA_SYTUACJI: str
    Powód_decyzji: str

class SMSMetadata(BaseModel):
    message: str
    to_number: str
    
class ChatRequest(BaseModel):
    req_type: str
    user_id: str
    prompt: str