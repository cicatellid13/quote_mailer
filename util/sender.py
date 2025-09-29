import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
import requests


load_dotenv()

# TODO add carrier hash map


def send_text_smtp(to_num: int, msg: str) -> bool:
    email = os.environ.get("gmail_from")

    msg_obj = EmailMessage()
    msg_obj.set_content(msg[:160])
    msg_obj["Subject"] = ""
    msg_obj["From"] = email
    msg_obj["To"] = f"{to_num}@vtext.com"
    email = os.environ.get("gmail_from")

    with smtplib.SMTP("smtp.gmail.com", port=587) as conn:
        conn.starttls()
        conn.login(
            user=email,
            password=os.environ.get("gmail_app_pw"),
        )

        result = conn.send_message(msg_obj)

        return True if not result else False


def send_sms_textr(to_num: int, msg: str) -> dict:
    url = os.environ.get("textr_api_url")
    payload = {
        "to": to_num,
        "message": msg,
        "apikey": f"{os.environ.get('textr_api_key')}",
    }
    with requests.Session() as session:
        response = session.post(url=url, json=payload)

    return response.json()
