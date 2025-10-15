""" "MongoDB Base Client Module
A base client for connecting to a MongoDB database.
"""

from typing import Optional, Any
import certifi
from pymongo import MongoClient as _MongoClient
import os


class MongoBaseClient:
    """
    A base client for connecting to a MongoDB database.
    """

    def __init__(self, mock_client: Optional[Any] = None):
        if not mock_client:
            self._client = _MongoClient(
                self._build_mongo_connection_url(), tlsCAFile=certifi.where()
            )
        else:
            self._client = mock_client

        self._db_name = os.environ.get("db_name")
        self._collection = None

    def get_client(self) -> None:
        return self._client

    def close_client(self) -> None:
        self._client.close()

    def get_database(self):
        return self._client.get_database(self._db_name)

    def get_collection(self, name: str):
        return self.get_database().get_collection(name)

    def find_one_document(
        self,
        data_filter: Optional[dict] = None,
        projection: Optional[dict] = None,
        collation: Optional[dict] = None,
    ) -> dict:
        if self._collection is None:
            raise ValueError(f"collection not set in {type(self)}")
        return self._collection.find_one(
            data_filter, projection=projection, collation=collation
        )

    def find_one_by_aggregation(
        self, pipeline: list, collation: Optional[dict] = None
    ) -> dict:
        document_cursor = self._collection.aggregate(
            pipeline, collation=collation
        )
        return next(document_cursor, None)

    def execute_ping_test(self):
        try:
            return self._client.admin.command("ping")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    @staticmethod
    def _build_mongo_connection_url() -> _MongoClient:
        usr = os.environ.get("db_usr")
        pwd = os.environ.get("db_pwd")
        cluster = os.environ.get("db_cluster")
        uri = os.environ.get("db_uri_options")
        app_name = os.environ.get("db_app_name")

        connection_url = (
            f"mongodb+srv://{usr}:{pwd}@{cluster}/" f"?{uri}={app_name}"
        )

        return connection_url
