from typing import Optional, Any
from mongo.mongo_user_data_collection import mongo_users_ctx
from util.schemas import UserDbSchema, UserDbAddUsedQuote


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
) -> bool:
    with mongo_users_ctx(mock_client=mock_client) as mongo:
        response = mongo.update_user_quotes_sent(document)

        if response:
            return True

    return False


def get_user(username: str, mock_client: Optional[Any] = None) -> UserDbSchema:
    with mongo_users_ctx(mock_client=mock_client) as mongo:
        response = mongo.get_user_document(username)

        return response
