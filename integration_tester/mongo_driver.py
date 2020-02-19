""" Mongo Driver Module.

This optional module extends the driver module to provide testing tools for
[MongoDB](https://www.mongodb.com/).

Typical usage is done through importing the module.
``` python
from integration_tester import mongo_driver

driver = mongo_driver.MongoDBDriver()
```

This module will raise a `OptionalModuleNotInstalledException` if the `pymongo`
package has not been installed.
"""
from integration_tester import driver, errors

# This module is an optional extra, this checks that the required packages are
# installed.
try:
    import pymongo
except ModuleNotFoundError as error:
    raise errors.OptionalModuleNotInstalled(
        "To support the optional MongoDB driver please install the pymongo"
        " package.") from error


class MongoDBDriver(driver.Driver):
    """ MongoDB Driver.

    This class extends the Docker driver to provide an interface for a MongoDB
    test instance.

    The most common implementation of the Class is to use the default settings.
    ``` python
    mongo = MongoDBDriver()
    ```

    This class has 3 noticeable features:
    1. Initialise a new Docker container instance of MongoDB on initialisation
       of this object.
    2. Ready check of the MongoDB service inside the container, not just the
       container itself.
    3. Reset the MongoDB instide the service to factory settings and not reset
       the container itself.

    If ensuring the container is reset completely each iteration, you can delete
    the existing container and start a new one.
    ``` python
    mongo = MongoDBDriver()
    del(mongo)
    mongo = MongoDBDriver()
    ```
    This will completely remove the container and its volume, then create a new
    container and volume.
    """
    def __init__(self,
                 tag: str = "3.4",
                 host: str = "127.0.0.1",
                 port: int = 27017):
        """ Initialise the MongoDB Driver.

        This will configure and then start the Docker container.

        Args:
            tag: Reference to the specific version of Docker Image to pull from
                 Docker Hub.
            host: Host address to bind the port.
            port: The port to bind the container.

        Container tags can be found on the
        [Docker Hub](https://hub.docker.com/_/mongo).
        """
        self.host, self.port = host, port
        ports = {27017: (host, port)}
        super().__init__(f"mongo:{tag}", ports)

    def ready(self) -> bool:
        """ Confirm if the MongoDB Service is running.

        Confirm if the MongoDB Service within the container is running and
        ready to accept connections. To achieve this, a `pymongo.MongoClient`
        object is created and the the server is polled using the `.server_info`
        method. This method serves no information purpose other than starting
        an active connection to the service.

        Returns:
            This function returns True if the MongoDB Service is active.
        """
        try:
            client = pymongo.MongoClient(f"{self.host}:{self.port}",
                                         serverSelectionTimeoutMS=100)
            client.server_info()
            return True
        except pymongo.errors.ConnectionFailure:
            return False

    def reset(self) -> None:
        """ Reset the database to factory new.

        This method soft resets the MongoDB Service within the container. This
        allows for a clean testing environment without the slow reset of Docker.
        However, this is not a completely isolated process. If complete
        isolation is required, please see Class doc on how to reset completely.
        """
        client = pymongo.MongoClient(f"{self.host}:{self.port}",
                                     serverSelectionTimeoutMS=100)
        for database in client.list_database_names():
            if database not in {"admin"}:
                for collection in client[database].list_collection_names():
                    client[database][collection].drop()
                client.drop_database(database)
