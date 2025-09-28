from util.quote_data_actions import get_quote_data_by_author
from util.user_data_actions import add_quote_to_user, get_user
import random
from util.schemas import UserDbAddUsedQuote

while True:
    username = input("username: ")
    user = get_user(username)

    if not user:
        print(f"no user found for {username}")
        break
    print("here")
    data = get_quote_data_by_author(
        author=user.author_choice,
        used_quotes=user.quotes_sent[user.author_choice],
    )

    choice_idx = random.randint(0, len(data.quotes) - 1)
    # print(f"length: {len(data.quotes)}")
    # print(f"choice: {choice_idx}")
    quote = data.quotes[choice_idx]
    print(f"{data.quotes[choice_idx]}\n\n -{data.author}")

    user_update = UserDbAddUsedQuote(
        username=user.username, author=user.author_choice, quote=quote
    )

    if add_quote_to_user(user_update):
        print("user updated")
    else:
        print("issue updating user")

    break
