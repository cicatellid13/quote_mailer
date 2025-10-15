"""
Mongo User Data Collection

user-data
"""

import os
from typing import Optional, Any, ContextManager
from contextlib import contextmanager
from mongo.mongo_base_client import MongoBaseClient
from pymongo.collection import InsertOneResult
from pymongo import ReturnDocument

from util.schemas import UserDbSchema, UserDbAddUsedQuote, UserDbUpdate


class MongoUserDataCollection(MongoBaseClient):
    """
    A client for connecting to the user-data collection in MongoDB.
    """

    def __init__(
        self,
        mock_client: Optional[Any] = False,
    ):
        super().__init__(mock_client=mock_client)
        self._collection = self.get_collection(os.environ.get("db_users_coll"))

    def create_user_document(self, document: UserDbSchema) -> InsertOneResult:

        if self._collection is None:
            raise ValueError(f"collection not set int {type(self)}")

        if not isinstance(document, UserDbSchema):
            raise ValueError(
                f"document must be of type UserDbSchema, received {type(document)}"
            )
        return self._collection.update_one(
            {"username": document.username},
            {
                "$set": {
                    "number": document.number,
                    "quotes_sent": document.quotes_sent,
                    "author_choice": document.author_choice,
                }
            },
            upsert=True,
        )

    def get_user_document(self, username):
        if self._collection is None:
            raise ValueError(f"collection not set int {type(self)}")

        document = self.find_one_document(
            data_filter={"username": username}, projection={"_id": False}
        )
        return UserDbSchema(**document)

    def update_user_quotes_sent(self, update_data: UserDbAddUsedQuote):
        if self._collection is None:
            raise ValueError(f"collection not set int {type(self)}")

        updated_document = self._collection.find_one_and_update(
            {"username": update_data.username},
            {
                "$addToSet": {
                    f"quotes_sent.{update_data.author}": update_data.quote
                }
            },
            return_document=ReturnDocument.AFTER,
        )

        if not updated_document:
            raise ValueError(f"User '{update_data.username}' not found")

        return updated_document

    def update_user_data(self, update_data: UserDbUpdate):
        if self._collection is None:
            raise ValueError(f"collection not set in {type(self)}")

        return self._collection.update_one(
            {"username": update_data.username},
            {"$set": update_data.model_dump(exclude_none=True)},
        )


@contextmanager
def mongo_users_ctx(
    mock_client: Optional[Any] = None,
) -> ContextManager[MongoUserDataCollection]:
    user_collection = MongoUserDataCollection(mock_client=mock_client)
    yield user_collection
    user_collection.close_client()
