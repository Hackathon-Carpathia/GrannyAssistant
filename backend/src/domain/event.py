from pydantic import BaseModel, Field
from typing import List
from datetime import date
from dataclasses import dataclass


class UserQuery(BaseModel):
    user_id: int
    question: str

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "question": self.question
        }


class RegisterEvent(BaseModel):
    user_id: int
    prompt: str
    start_date: date
    end_date: date
    hours: List[int]

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "prompt": self.prompt,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "hours": self.hours
        }


class Event(BaseModel):
    user_id: int
    prompt: str

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "prompt": self.prompt
        }

@dataclass
class LLMResponse():
    user_id: int
    message: str

    @classmethod
    def from_dict(cls, data: dict) -> 'LLMResponse':
        return cls.model_validate(data)