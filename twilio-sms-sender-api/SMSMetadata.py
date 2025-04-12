from pydantic import BaseModel


class SMSMetadata(BaseModel):
    message: str
    to_number: str
