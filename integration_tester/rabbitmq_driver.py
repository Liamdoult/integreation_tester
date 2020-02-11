try:
    import pika
except ModuleNotFoundError as error:
    raise Exception("To support MongoDB please install the mongo package"
                    " optional extra.") from error

from integration_tester import driver


class RabbitMQDriver(driver.Driver):

    def __init__(self, tag: str = "latest", host: str = "127.0.0.1",
                 port: int = 5672, username: str = "guest",
                 password: str = "guest"):
        self.host, self.port = host, port
        self.username, self.password = username, password
        ports = {5672: (host, port)}
        super().__init__(f"rabbitmq:{tag}", ports)

    def ready(self):
        """ Check if RabbitMQ has started.

        This function returns True if the RabbitMQ service within the container
        is running and ready to accept connections.
        """
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host,
            self.port,
            '/',
            credentials
        )
        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.IncompatibleProtocolError as error:
            return False
        connected = connection.is_open
        connection.close()
        return connected

    def reset(self, queues):
        """ Reset RabbitMQ to factory new. """
        # TODO(Liam) this requires the user to provide each queue. There is no
        # way to check what queues have been created and the relies on the user
        # reseting the queue. Check if there is another way to do this.
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host,
            self.port,
            '/',
            credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        for queue in queues:
            channel.queue_delete(queue=queue)
