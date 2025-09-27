"""
Mongo Quote Data Collection

quote-data
"""

from typing import Optional, Any
from mongo.mongo_base_client import MongoBaseClient


class MongoQuoteDataCollection(MongoBaseClient):
    """A client for connecting to the quote-data collection in MongoDB.

    :param mock_client
    :ptype: str, optional
    :param ping_test: bool, optional
    :param coll_name: str,
    :param db_name: str,

    returns: nothing
    """

    def __init__(
        self,
        coll_name: str,
        db_name: str,
        mock_client: Optional[Any] = False,
        ping_test: bool = False,
    ):
        super().__init__(
            mock_client=mock_client,
            ping_test=ping_test,
            coll_name=coll_name,
            db_name=db_name,
        )
