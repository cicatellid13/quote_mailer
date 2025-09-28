from typing import Optional, Any
from mongo.mongo_quote_data_collection import mongo_quote_ctx
from util.schemas import QuoteDbSchema
from util.data_scrapers.tomlin_quotes import get_quotes


def get_quote_data() -> QuoteDbSchema:
    data = get_quotes()
    cleaned = [d.replace(data["author"], "").strip() for d in data["quotes"]]

    return QuoteDbSchema(author=data["author"], quotes=cleaned)


def update_quote_data(
    document: QuoteDbSchema, mock_client: Optional[Any] = None
) -> bool:
    with mongo_quote_ctx(mock_client=mock_client) as mongo:
        response = mongo.create_quote_document(document)

        if response.acknowledged:
            return True

    return False


def get_quote_data_by_author(
    author: str,
    used_quotes: Optional[list] = None,
    mock_client: Optional[Any] = None,
) -> QuoteDbSchema:
    with mongo_quote_ctx(mock_client=mock_client) as mongo:
        response = mongo.get_quote_data_by_author(author, used_quotes)

        return response


def get_and_load_data() -> bool:
    data_to_load = get_quote_data()

    if update_quote_data(data_to_load):
        return True
    return False
