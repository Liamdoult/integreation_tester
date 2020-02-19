""" Redis Driver Module.

This optional module extends the driver module to provide testing tools for
[Redis](https://redis.io/).

Typical usage is done through importing the module.
``` python
from integration_tester import redis_driver

driver = redis_driver.RedisDriver()
```

This module will raise a `OptionalModuleNotInstalledException` if the `redis`
package has not been installed.
"""
from integration_tester import driver, errors

try:
    import redis
except ModuleNotFoundError as error:
    raise errors.OptionalModuleNotInstalled(
        "To support the optional Redis Driver please install the redis"
        " package.") from error


class RedisDriver(driver.Driver):
    """ Redis Driver.

    This class extends the Docker driver to provide an interface for a Redis
    test instance.

    The most common implementation of the Class is to use the default settings.
    ``` python
    redis = RedisDriver()
    ```

    This class has 3 noticeable features:
    1. Initialise a new Docker container instance of Redis on initialisation
       of this object.
    2. Ready check of the Redis service inside the container, not just the
       container itself.
    3. Reset the Redis instide the service to factory settings and not reset
       the container itself.

    If ensuring the container is reset completely each iteration, you can delete
    the existing container and start a new one.
    ``` python
    redis = RedisDriver()
    del(redis)
    redis = RedisDriver()
    ```
    This will completely remove the container and its volume, then create a new
    container and volume.
    """
    def __init__(self,
                 tag: str = "5.0.7",
                 host: str = "127.0.0.1",
                 port: str = 6379):
        """ Initialise the Redis Driver.

        This will configure and then start the Docker container.

        Args:
            tag: Reference to the specific version of Docker Image to pull from
                 Docker Hub.
            host: Host address to bind the port.
            port: The port to bind the container.

        Container tags can be found on the
        [Docker Hub](https://hub.docker.com/_/redis).
        """
        self.host, self.port = host, port

        ports = {6379: (self.host, self.port)}
        super().__init__(f"redis:{tag}", ports)

    def ready(self) -> bool:
        """ Confirm if the Redis Service is running.

        Confirm if the Redis Service within the container is running and ready
        to accept connections. To achieve this, a `redis.Redis` object is
        created and the the server is polled using the `.client_list` method.
        This method serves no information purpose other than starting an active
        connection to the service.

        Returns:
            This function returns True if the Redis Service is active.
        """
        try:
            instance = redis.Redis(self.host, self.port, db=0)
            instance.client_list()
            return True
        except redis.ConnectionError:
            return False

    def reset(self):
        """ Reset the database to factory new.

        This method soft resets the Redis Service within the container. This
        allows for a clean testing environment without the slow reset of
        Docker. However, this is not a completely isolated process. If complete
        isolation is required, please see Class doc on how to reset completely.
        """
        instance = redis.Redis(self.host, self.port)
        instance.flushall()
