from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()


class Number():
    def __init__(self, target):
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        account_token = os.environ.get('TWILIO_ACCOUNT_TOKEN')
        self.client = Client(account_sid, account_token)

        self.number = os.environ.get(
            'TWILIO_REGION_CODE') + os.environ.get('TWILIO_NUMBER')
        self.target_number = target

    def send_message(self, message_body):
        return self.client.messages.create(
            to=self.target_number,
            from_=self.number,
            body=message_body
        )

    def read_messages(self):
        return reversed(self.client.messages.list())

    @staticmethod
    def print_message(m):
        print(f'[{m.from_}] : {m.body}')


if __name__ == '__main__':
    target_number = os.environ.get(
        'REDIRECT_REGION_CODE') + os.environ.get('REDIRECT_NUMBER')
    a = Number(target_number)

    messages = a.read_messages()
    for m in messages:
        a.print_message(m)
