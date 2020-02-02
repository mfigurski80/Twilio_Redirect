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

        self.dir_path = os.environ.get('HOME_DIR')

    def send_message(self, message_body, target_number=None):
        if target_number is None:
            target_number = self.target_number
        return self.client.messages.create(
            to=target_number,
            from_=self.number,
            body=message_body
        )

    def get_messages(self):
        return list(reversed(self.client.messages.list()))

    def get_conversations(self):
        messages = self.get_messages()
        conversations = {}
        for m in messages:
            # get conversant
            conversant = m.to
            if conversant == self.number:
                conversant = m.from_
            # enter into respective conversation
            if conversant not in conversations:
                conversations[conversant] = []
            conversations[conversant] += [m]
        return conversations

    def get_new_conversations(self):
        conversations = self.get_conversations()
        seen = self.read_seen_conversations()
        processed_conversations = {}
        for conv in conversations:
            if conv in seen and seen[conv] < len(conversations[conv]):
                # show last three as well
                # FIXME: doesn't work somehow? Just generally shows however many it wants to
                processed_conversations[conv] = conversations[conv][seen[conv] - 3:]
        self.write_seen_conversations(conversations)
        return processed_conversations

    def write_seen_conversations(self, conversations):
        with open(self.dir_path + '/seen.txt', 'w') as f:
            f.write('\n'.join([c + ', ' + str(len(conversations[c]))
                               for c in conversations]))
            f.close()

    def read_seen_conversations(self):
        try:
            with open(self.dir_path + '/seen.txt', 'r') as f:
                content = f.read().split('\n')
                f.close()
                num_conversations = {}
                for line in content:
                    conv = line.split(', ')
                    num_conversations[conv[0]] = int(conv[1])
                return num_conversations
        except:
            return {}

    @staticmethod
    def stringify_conversation(conversation):
        ret = ''
        for conv in conversation:
            ret += f'[{conv}]\n'
            for m in conversation[conv]:
                is_user = (m.from_ == conv)
                if not is_user:
                    ret += '\033[1m'
                ret += f'"{m.body}"\033[0m \n'
        return ret


if __name__ == '__main__':
    import sys

    target_number = os.environ.get(
        'REDIRECT_REGION_CODE') + os.environ.get('REDIRECT_NUMBER')
    a = Number(target_number)

    print(a.stringify_conversation(a.get_new_conversations()))

    # if len(sys.argv) > 1:
    #     args = sys.argv[1:]
    #     number = None
    #     message = ' '.join(args)

    #     # check if first arg is a phone number...
    #     if args[0][1:].isdigit() and len(args[0]) >= 10:
    #         number = args[0]
    #         message = ' '.join(args[1:])
    #         if not number[0] is '+':
    #             number = f'+1{number}'

    #     a.send_message(message, number)

    # else:
    #     print(a.stringify_conversation(a.get_new_conversations()))
