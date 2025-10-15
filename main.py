from util.quote_data_actions import get_quote_data_by_author
from util.user_data_actions import add_quote_to_user, get_user
import random
from util.schemas import UserDbAddUsedQuote
from util.sender import send_text_smtp
from util.twilio_base_client import TwilioClient
import logging

while True:
    username = input("username: ")
    user = get_user(username)

    if not user:
        print(f"no user found for {username}")
        break

    sender = TwilioClient()
    data = get_quote_data_by_author(
        author=user.author_choice,
        used_quotes=user.quotes_sent.get(user.author_choice, {}),
    )

    choice_idx = random.randint(0, len(data.quotes) - 1)
    quote = data.quotes[choice_idx]
    msg = f"{data.quotes[choice_idx]}\n\n -{data.author}"

    sent = send_text_smtp(user.number, msg)
    # sent = sender.send_sms(user.number, msg)
    print(sent)
    print("msg sent: \n", msg, "\n")

    user_update = UserDbAddUsedQuote(
        username=user.username, author=user.author_choice, quote=quote
    )

    if add_quote_to_user(user_update):
        print(user.username, "updated")
    else:
        print("issue updating user", user.username)
    break
