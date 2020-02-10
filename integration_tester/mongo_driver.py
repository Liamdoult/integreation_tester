from typing import Optional

try:
    # MongoDB specific imports. These need to be installed to use the mongo
    # feature. This is to limit installing unessesarry libraries.
    # TODO(Liam) Automate the downloading for this feature.
    import pymongo
except ModuleNotFoundError as error:
    raise Exception("To support MongoDB please install the mongo package"
                    " optional extra.") from error

from integration_tester import driver


class MongoDBDriver(driver.Driver):

    def __init__(self, version: str = "3.4", host: Optional[str] = "127.0.0.1",
                 port: Optional[int] = 27017):
        self.host, self.port = host, port
        ports = {27017: (host, port)}
        super().__init__(f"mongo:{version}", ports)

    def ready(self) -> bool:
        """ Check if MongoDB has started.

        This function returns True if the MongoDB Service within the container
        is running and ready to accept connections.
        """
        try:
            client = pymongo.MongoClient(f"{self.host}:{self.port}", serverSelectionTimeoutMS=100)
            client.server_info()
            return True
        except pymongo.errors.ConnectionFailure:
            return False

    def reset(self): 
        """ Reset the database to factory new. """
        # TODO(Liam) Version Support (2.4 and earlier)
        # TODO(Liam) Protected databases and collections
        # TODO(Liam) Ensure no data was added to the other tables
        # TODO(Liam) Ensure that custom settings are reset
        client = pymongo.MongoClient(f"{self.host}:{self.port}", serverSelectionTimeoutMS=100)
        for database in client.list_database_names():
            if database not in {"admin"}:
                for collection in client[database].list_collection_names():
                    client[database][collection].drop()
                client.drop_database(database)
