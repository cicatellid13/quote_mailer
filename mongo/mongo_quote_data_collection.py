"""
Mongo Quote Data Collection

quote-data
"""

import os
from typing import Optional, Any, ContextManager
from contextlib import contextmanager
from mongo.mongo_base_client import MongoBaseClient
from pymongo.collection import InsertOneResult
from dotenv import load_dotenv

from util.schemas import QuoteDbSchema


load_dotenv()


class MongoQuoteDataCollection(MongoBaseClient):
    """
    A client for connecting to the quote-data collection in MongoDB.
    """

    def __init__(
        self,
        mock_client: Optional[Any] = False,
    ):
        super().__init__(mock_client=mock_client)
        self._collection = self.get_collection(
            os.environ.get("db_quotes_coll")
        )

    def create_quote_document(
        self, document: QuoteDbSchema
    ) -> InsertOneResult:

        if self._collection is None:
            raise ValueError(f"collection not set int {type(self)}")

        if not isinstance(document, QuoteDbSchema):
            raise ValueError(
                f"document must be of type QuoteDbSchema, received {type(document)}"
            )

        return self._collection.update_one(
            {"author": document.author},
            {"$set": {"quotes": document.quotes}},
            upsert=True,
        )

    def get_quote_data_by_author(
        self, author: str, used_quotes: Optional[list] = None
    ) -> QuoteDbSchema:

        if used_quotes:
            pipeline = [
                {"$match": {"author": author}},
                {
                    "$project": {
                        "author": 1,
                        "quotes": {
                            "$filter": {
                                "input": "$quotes",
                                "as": "q",
                                "cond": {
                                    "$not": [{"$in": ["$$q", used_quotes]}]
                                },
                            }
                        },
                    }
                },
            ]
            cursor = self._collection.aggregate(pipeline=pipeline)

            try:
                document = next(cursor)
            except StopIteration:
                return None

            if next(cursor, None) is not None:
                raise ValueError(
                    f"Multiple documents found for author '{author}'"
                )

        else:
            document = self.find_one_document(data_filter={"author": author})

        if document is None:
            return None

        return QuoteDbSchema(**document)


@contextmanager
def mongo_quote_ctx(
    mock_client: Optional[Any] = None,
) -> ContextManager[MongoQuoteDataCollection]:
    quote_collection = MongoQuoteDataCollection(mock_client=mock_client)
    yield quote_collection
    quote_collection.close_client()
