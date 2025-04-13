import os
from fastapi import APIRouter, Depends
from src.twilio_config import get_twilio_client
from src.SMSMetadata import SMSMetadata
from dotenv import load_dotenv

router = APIRouter()

load_dotenv(override=True)

@router.post("/sendSMS/", tags=["SMS"])
async def send_sms(sms_data: SMSMetadata, twilio=Depends(get_twilio_client)) -> str:
    print(f"sms_data {sms_data.message}")
    print(f"os + {os.getenv('FROM_NUMBER')}")
    print(f"TO + {sms_data.to_number}")
    message = twilio.messages.create(
        body=sms_data.message,
        from_=os.getenv("FROM_NUMBER"),
        to=sms_data.to_number,
    )
    print(f"SMS sent successfully - {message.sid}")
    return f"SMS sent successfully - {message.sid}"