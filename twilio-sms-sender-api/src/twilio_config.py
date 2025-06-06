import os
from twilio.rest import Client

from dotenv import load_dotenv

load_dotenv(override=True)



def get_twilio_client():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    return client
