from pydantic import BaseModel

class UserRequest(BaseModel):
    req_type: str
    user_id: str
    prompt: str