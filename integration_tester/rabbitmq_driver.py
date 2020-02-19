""" RabbitMQ Driver Module.

This optional module extends the driver module to provide testing tools for
[RabbitMQ](https://www.rabbitmq.com/).

Typical usage is done through importing the module.
``` python
from integration_tester import rabbitmq_driver

driver = rabbitmq_driver.RabbitMQDriver()
```

This module will raise a `OptionalModuleNotInstalledException` if the `pika`
package has not been installed.
"""
from typing import List

from integration_tester import driver, errors

try:
    import pika
except ModuleNotFoundError as error:
    raise errors.OptionalModuleNotInstalled(
        "To support the optional RabbitMQ Driver please install the pika"
        " package.") from error


class RabbitMQDriver(driver.Driver):
    """ RabbitMQ Driver.

    This class extends the Docker driver to provide an interface for a RabbitMQ
    test instance.

    The most common implementation of the Class is to use the default settings.
    ``` python
    rabbitmq = RabbitMQDriver()
    ```

    This class has 3 noticeable features:
    1. Initialise a new Docker container instance of RabbitMQ on initialisation
       of this object.
    2. Ready check of the RabbitMQ service inside the container, not just the
       container itself.
    3. Reset the RabbitMQ instide the service to factory settings and not reset
       the container itself.

    If ensuring the container is reset completely each iteration, you can delete
    the existing container and start a new one.
    ``` python
    rabbitmq = RabbitMQDriver()
    del(rabbitmq)
    rabbitmq = RabbitMQDriver()
    ```
    This will completely remove the container and its volume, then create a new
    container and volume.
    """
    def __init__(self,
                 tag: str = "latest",
                 host: str = "127.0.0.1",
                 port: int = 5672,
                 username: str = "guest",
                 password: str = "guest"):
        """ Initialise the RabbitMQ Driver.

        This will configure and then start the Docker container.

        Args:
            tag: Reference to the specific version of Docker Image to pull from
                 Docker Hub.
            host: Host address to bind the port.
            port: The port to bind the container.
            username: Connection authentication username to configure the
                      service with.
            password: Connection authentication password to configure the
                      service with.

        Container tags can be found on the
        [Docker Hub](https://hub.docker.com/_/rabbitmq).
        """
        self.host, self.port = host, port
        self.username, self.password = username, password

        ports = {5672: (host, port)}
        super().__init__(f"rabbitmq:{tag}", ports)

    def ready(self) -> bool:
        """ Confirm if the RabbitMQ Service is running.

        Confirm if the RabbitMQ Service within the container is running and
        ready to accept connections. To achieve this, a
        `pika.BlockingConnection` object is created and the the server is
        polled using the `.is_open` method.  This method serves no information
        purpose other than starting an active connection to the service.

        Returns:
            This function returns True if the RabbitMQ Service is active.
        """
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, '/',
                                               credentials)

        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            return False

        connected = connection.is_open
        connection.close()
        return connected

    def reset(self, queues: List[str]) -> None:
        """ Reset the database to factory new.

        *NB*: Please provide *ALL* queues created within your code to ensure a
        proper reset.

        This method soft resets the RabbitMQ Service within the container. This
        allows for a clean testing environment without the slow reset of
        Docker. However, this is not a completely isolated process. If complete
        isolation is required, please see Class doc on how to reset completely.

        Args:
            queues: List of queues creating during usage of the instance.

        This method currently relies on the user to provide accurate queue
        information as there is no way to check what queues have been created
        and the names of the created queues are required to reset the service.
        """
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, '/',
                                               credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        for queue in queues:
            channel.queue_delete(queue=queue)
