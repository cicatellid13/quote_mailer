from typing import Optional, Any
from mongo.mongo_quote_data_collection import mongo_quote_ctx
from util.schemas import QuoteDbSchema
from util.data_scrapers.brainy_quotes import get_quotes_by_author


def get_quote_data(author: str) -> QuoteDbSchema:
    data = get_quotes_by_author(author)
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


def get_and_load_data(author: str) -> bool:
    data_to_load = get_quote_data(author)

    if len(data_to_load.quotes) > 0 and update_quote_data(data_to_load):
        return True
    return False
