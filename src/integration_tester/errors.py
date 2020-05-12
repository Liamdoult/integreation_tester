""" Error Handling Module

This module contains all error handling classes.
"""


class DockerNotAvailable(Exception):
    """ Docker Not Available Exception.

    This exception is raised when Docker is (a) not configured correctly or (b)
    is not running on the local machine.

    Attr:
        MESSAGE: Message constant used as a standard error message template.
    """
    MESSAGE = ("Failed to connect to Docker. Please ensure Docker is correctly"
               " configured and running.")

    def __init__(self):
        super().__init__(self, self.MESSAGE)


class OptionalModuleNotInstalled(Exception):
    """ Optional Module Not Installed Exception.

    This exception is raised when using an optional driver that does not have
    all the required packages installed.
    """


class ReadyTimeout(Exception):
    """ Read Timeout Exception.

    This exception is raised when the `wait_until_ready` timesout.
    """
