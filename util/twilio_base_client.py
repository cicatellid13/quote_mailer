from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


class TwilioClient:
    def __init__(self, body: str, to_num: str, from_num: str):
        self.auth_token = os.environ.get("twilio_auth_token")
        self.sid = os.environ.get("twilio_sid")
        self.client = Client(self.sid, self.auth_token)
        self.from_number = from_num
        self.to_number = to_num
        self.body = body

    def send_sms(self):
        try:
            message = self.client.messages.create(
                body=self.body,
                from_=self.from_number,
                to=self.to_number,
            )
            print(f"Message SID: {message.sid}")
            print(f"Message status: {message.status}")
        except Exception as e:
            print(f"Error sending message: {e}")
