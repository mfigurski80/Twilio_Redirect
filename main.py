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

    def send_message(self, message_body, target_number=None):
        if target_number is None:
            target_number = self.target_number
        return self.client.messages.create(
            to=target_number,
            from_=self.number,
            body=message_body
        )

    def read_messages(self):
        return list(reversed(self.client.messages.list()))

    def read_new_messages(self):
        messages = self.read_messages()
        num_seen = self.read_seen()
        self.write_seen(len(messages))
        return messages[num_seen:]

    @staticmethod
    def print_message(m):
        print(f'[{m.from_}] : {m.body}')

    def read_seen(self):
        with open('seen.txt', 'r') as f:
            content = f.read()
            f.close()
            content = int(content)
            return content

    def write_seen(self, seen):
        with open('seen.txt', 'w') as f:
            f.write(str(seen))
            f.close()


if __name__ == '__main__':
    import sys

    target_number = os.environ.get(
        'REDIRECT_REGION_CODE') + os.environ.get('REDIRECT_NUMBER')
    a = Number(target_number)

    if len(sys.argv) > 1:
        args = sys.argv[1:]
        number = None
        message = ' '.join(args)

        # check if first arg is a phone number...
        if args[0][1:].isdigit() and len(args[0]) >= 10:
            number = args[0]
            message = ' '.join(args[1:])
            if not number[0] is '+':
                number = f'+1{number}'

        a.send_message(message, number)

    else:
        messages = a.read_new_messages()
        for m in messages:
            a.print_message(m)
