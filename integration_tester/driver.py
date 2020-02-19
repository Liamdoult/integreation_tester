""" Underlying Abstraction module for Docker.

This module abstracts [Python
Docker](https://docker-py.readthedocs.io/en/stable/) by wrapping it in a
`Driver` Class. This class forms the foundation of all different application
drivers. This is the primary module of the project.

Typical interfacing is done through inheritance.
``` python
from integration_tester import driver

class SomeNewDriver(driver.Driver):
    ...
```

This module will raise a `DockerNotAvailable` exception on import if Docker is
not running or incorrectly configured.
"""
import time
from typing import Dict, Optional, Tuple, Union

import docker

from integration_tester import errors

CLIENT = docker.from_env()

# Test Docker client connection
try:
    CLIENT.images.list()
except Exception as error:
    raise errors.DockerNotAvailable() from error


class Driver:
    """ Base Docker Abstraction.

    This Class abstracts the Python Docker SDK by starting, stopping and
    cleaning Docker containers and images. This driver should only be used as a
    base Class to other higher level Classes.
    """
    _status = True

    def __init__(self,
                 tag: str,
                 ports: Optional[Dict[int, Tuple[str, int]]] = None,
                 remove_image: bool = False):
        """ Initialise the driver.

        Initialisation includes creating and starting a detached instance of
        the Docker container associated to the `tag` provided.

        Args:
            tag: Reference to the specific version of Docker Image to pull from
                 Docker Hub.
            ports: Ports to expose from the container.
            remove_image: Flag to delete the Docker Image from the local machine
                          on object deconstruction.

        Tags refer to the Docker Image version "tag" which can be found on the
        [Docker Hub](https://hub.docker.com/) for any given public image.

        Ports should be provided in the following format:
        ``` python
        {
            port_from: (address_to, port_to),
        }
        ```
        This will bind `port_from` to the address `address_to` and to the port
        `port_to`. I.E. `port_from` -> `address_to:port_to`.
        """
        self.tag = tag
        self._remove_image = remove_image

        self._ports = {}
        if ports is not None:
            self._ports = ports

        self._container = CLIENT.containers.run(self.tag,
                                                detach=True,
                                                ports=self._ports)

    def __del__(self) -> None:
        """ Ensure proper removal of docker resources.

        The container and its associated volume is stopped and *Force* deleted.

        If `_remove_image` is set to True on initialisation this will delete
        the downloaded (or existing) local image. This is a soft delete
        (Meaning if there is an already linked container existing, it will
        *not* delete the image). This is to ensure that we don't get any "YouR
        CoDe BroKE mY dAtA ConTainEr" messages.
        """
        # Image needs to be retrieved prior to container object deconstruction.
        image = self._container.image

        self._container.stop()
        self._container.remove(v=True, force=True)

        # Image needs to be deleted after container deconstruction due to
        # referencing issues.
        if self._remove_image is True:
            try:
                CLIENT.images.remove(image.id)
            except docker.errors.APIError as error:
                if error.status_code != 409:
                    raise error

    def ready(self) -> bool:
        """ Container ready check.

        This method *should* be overridden.

        This method should return `True` when the software inside the container
        has correctly loaded and is ready to receive connections.
        """
        return self._status

    # Pylint disabled: this method should be overridden and `self` may be
    # required.
    def reset(self) -> bool:  # pylint: disable=R0201
        """ Reset the service.

        This method *should* be override.

        This method should reset the software inside the container to `factory`
        settings (original state).
        """
        return

    def wait_until_ready(self,
                         wait_interval: Union[float, int] = 1,
                         timeout: int = 60) -> None:
        """ Block until container is ready to be used.

        This blocking method extends `ready`. This means that it is not just a
        check of when the Docker container is running but when the software
        inside the container is "ready". i.e. Docker says the MongoDB container
        is ready but the mongo application inside the container is starting.

        Args:
            wait_interval: Gaps between checks of the container (Not
                           recommended to change).
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
