from twilio.rest import Client
import os
from dotenv import load_dotenv
import logging

load_dotenv()


class TwilioClient:
    def __init__(self):
        self._api_key = os.environ.get("twilio_api_key")
        self._api_secret = os.environ.get("twilio_api_secret")
        self._client = Client(
            username=self._api_key, password=self._api_secret
        )
        self._from_number = os.environ.get("twilio_from")

    def send_sms(self, to_number: str, body: str) -> str:
        try:

            message = self._client.messages.create(
                body=body,
                from_=self._from_number,
                to=self._set_number_country_code(to_number),
            )
            return message.sid
        except Exception as e:
            logging.error(f"Failed to send SMS to {to_number}: {e}")

            raise RuntimeError(f"Error sending message to {to_number}") from e

    def _set_number_country_code(self, number: str) -> str:
        if number.startswith("1"):
            return f"+{number}"
        return f"+1{number}"

    def get_message_status(self, msg_sid: str) -> str:
        message = self._client.messages(msg_sid).fetch()
        return message.status
