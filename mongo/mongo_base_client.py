""" "MongoDB Base Client Module
A base client for connecting to a MongoDB database.
"""

from urllib.parse import quote_plus
from typing import Optional, Any
import certifi
from pymongo import MongoClient


class MongoBaseClient:
    """A base client for connecting to a MongoDB database.
    param mock_client Optional[Any], optional
    param ping_test: bool, optional
    param usr: Optional[str], optional
    param pwd: Optional[str], optional
    param cluster: Optional[str], optional
    param coll_name: Optional[str], optional
    param db_name: Optional[str], optional
    param app_name: Optional[str], optional

    returns: nothing, meant to be inherited

    Raises
    ------
    ValueError
        If required parameters are missing when mock_client is not provided.
    ConnectionError
        If the ping test fails when ping_test is enabled.
    """

    def __init__(
        self,
        mock_client: Optional[Any] = False,
        ping_test: bool = False,
        usr: Optional[str] = None,
        pwd: Optional[str] = None,
        cluster: Optional[str] = None,
        coll_name: Optional[str] = None,
        db_name: Optional[str] = None,
        app_name: Optional[str] = None,
        uri_options: Optional[str] = None,
    ):
        self.mock_client = mock_client
        self.usr = usr
        self.pwd = pwd
        self.cluster = cluster
        self.coll_name = coll_name
        self.db_name = db_name
        self.app_name = app_name
        self.uri_options = uri_options

        # Validate inputs
        if not self.mock_client and not all(
            [usr, pwd, cluster, coll_name, db_name, app_name]
        ):
            raise ValueError(
                "Missing required parameters: usr, pwd, cluster, coll_name, db_name, app_name"
            )

        # Initialize client
        if mock_client:
            self.mock_client = mock_client
            self.client = mock_client
        else:
            self.client = self._get_client()

        # db collection
        self.db = self.client[self.db_name]
        self._collection = self.db[self.coll_name]

    def _get_client(self) -> MongoClient:
        password = quote_plus(str(self.pwd))
        connection_url = (
            f"mongodb+srv://{self.usr}:{password}@{self.cluster}/"
            f"?{self.uri_options}={self.app_name}"
        )

        return MongoClient(connection_url, tlsCAFile=certifi.where())

    def execute_ping_test(self):
        if self.ping_test:
            try:
                print("Successfully connected to MongoDB!")
                return self.client.admin.command("ping")
            except Exception as e:
                raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"db={getattr(self.db, 'name', None)!r}, "
            f"collection={getattr(self._collection, 'name', None)!r})"
        )
