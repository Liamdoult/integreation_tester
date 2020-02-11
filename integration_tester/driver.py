import re
import socket
import time
from typing import Dict, Optional, Union

import docker

from integration_tester import errors


# Test if docker is available
try:
    CLIENT = docker.from_env()
    CLIENT.images.list()
except Exception as e:
    raise Exception("Failed to setup docker connection. Please ensure you have"
            " configured docker correctly and that it is running.") from e

class Driver:
    """ Base driver to provide functionality to higher level drivers.

    This driver should only be used as a base class to other drivers. This
    driver handles docker and requires certain functions to be oferridden.
    """
    _status = True

    def __init__(self, tag: str, ports: Dict[int, None] = {},
                 remove_image: bool = False):
        """ Initialise the driver.

        Inintialisation includes running docker.

        Args:
            tag: The docker image to pull from dockerhub.
            host: Address to bind.
            ports: Ports to expose from the container.
        """
        self._tag = tag 
        self._remove_image = remove_image

        self._container = CLIENT.containers.run(self._tag, detach=True, ports=ports)

    def __del__(self) -> None:
        """ Ensure proper removal of docker resources.
        
        The container and its accociated volume is stopped and *Force* deleted.
        If `_remove_image` is set to True on initialisation this will delete
        the downloaded (or existing) local image.
        """
        # Image needs to be retrieved prior to container object deconstruction.
        image = self._container.image

        self._container.stop()
        self._container.remove(v=True, force=True)

        # Image needs to be deleted after container deconstruction due to
        # referencing issues.
        if self._remove_image is True:
            # TODO(Liam) Images that have been used for other containers will
            # fail to be deleted due to link to other containers. How should we
            # handle this?
            # Error: docker.errors.APIError: 409 Client Error: Conflict
            # ("conflict: unable to delete ccc6e87d482b (must be forced) -
            # image is being used by stopped container b7c4fef9694d")
            CLIENT.images.remove(image.id)

    def ready(self) -> bool:
        """ Container ready check.

        This function should be overridden. This function is used to confirm
        if the container is ready for testing.
        """
        return self._status 

    def reset(self) -> bool:
        """ Reset the service.

        This function should be overridde. This function is used to reset
        (through software) the service to its original state.
        """
        return True

    def wait_until_ready(self, wait_interval: Union[float, int] = 1,
                         timeout: int = 60) -> None:
        """ Block until container is ready to be used.

        This blocking method is based on `ready` and not docker. This means
        that it is not just a check of when docker has started the container
        but when the software inside the container is "ready". i.e. Docker says
        the mogno container is ready but the mongo application inside the
        container has not started.

        Args:
            wait_interval: Gaps between checks of the container.
            timeout: Timeout if the container does not become `ready`.
        """
        start_time = time.time()
        while not self.ready():
            interval = time.time() - start_time

            if interval >= timeout:
                raise errors.ReadyTimeout("Container failed to start.")

            # Make sure the wait will not be longer than the timeout
            if timeout - interval < wait_interval:
                time.sleep(timeout - interval)
            else:
                time.sleep(wait_interval)
