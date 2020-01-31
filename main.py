from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
account_token = os.environ.get('TWILIO_ACCOUNT_TOKEN')

print(account_sid)
print(account_token)
