try:
    import redis
except ModuleNotFoundError as error:
    raise Exception("To support MongoDB please install the mongo package"
                    " optional extra.") from error

from integration_tester import driver


class RedisDriver(driver.Driver):

    def __init__(self, version: str = "5.0.7", host: str = "127.0.0.1",
                 port: str = 6379):
        self.host = host
        self.port = port

        ports = {
            6379: (self.host, self.port)
        }

        super().__init__(f"redis:{version}", ports)

    def ready(self) -> bool:
        """ Check if Redis database has started.

        This function returns `True` if the Redis service within the container
        is running and ready to accept connections.
        """
        try:
            instance = redis.Redis(self.host, self.port, db=0)
            instance.client_list()
            return True
        except redis.ConnectionError:
            return False

    def reset(self):
        """ Reset the database to factory new. """
        instance = redis.Redis(self.host, self.port)
        instance.flushall()
