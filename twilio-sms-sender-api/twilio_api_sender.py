import os

from fastapi import Depends
from twilio_config import get_twilio_client
from SMSMetadata import SMSMetadata
from fastapi import FastAPI

app = FastAPI()


@app.post("/sendSMS/", tags=["SMS"])
async def send_sms(SMS_data: SMSMetadata, twilio=Depends(get_twilio_client)) -> str:
    message = twilio.messages.create(
        body=SMS_data.message,
        from_=os.getenv("FROM_NUMBER"),
        to=SMS_data.to_number,
    )
    return f"SMS send successfully - {message.sid}"
