from pydantic import BaseModel, Field
from typing import List
from datetime import date


class UserQuery(BaseModel):
    user_id: int
    question: str

class RegisterEvent(BaseModel):
    user_id: int
    prompt: str
    start_date: date
    end_date: date
    hours: List[int]

class Event(BaseModel):
    user_id: int
    prompt: str
