from typing import Optional, Any
from mongo.mongo_user_data_collection import mongo_users_ctx
from util.schemas import UserDbSchema, UserDbAddUsedQuote
from util.data_scrapers.tomlin_quotes import get_quotes


def get_quote_data() -> UserDbSchema:
    data = get_quotes()
    cleaned = [d.replace(data["author"], "").strip() for d in data["quotes"]]

    return UserDbSchema(author=data["author"], quotes=cleaned)


def update_user_data(
    document: UserDbSchema, mock_client: Optional[Any] = None
) -> bool:
    with mongo_users_ctx(mock_client=mock_client) as mongo:
        response = mongo.create_user_document(document)

        if response.acknowledged:
            return True

    return False


def add_quote_to_user(
    document: UserDbAddUsedQuote, mock_client: Optional[Any] = None
):
    with mongo_users_ctx(mock_client=mock_client) as mongo:
        response = mongo.update_user_quotes_sent(document)

        if response:
            return True

    return False
