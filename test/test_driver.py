import traceback

import docker
import pytest

from integration_tester import driver, errors


def test_driver_standard():
    """ Standard driver use test. """
    tag = "ubuntu:latest"
    drive = driver.Driver(tag)
    id = drive._container_id
    assert drive.ready() == True
    assert drive.reset() is None
    assert drive.wait_until_ready(timeout=10) is None
    drive._status = False
    with pytest.raises(errors.ReadyTimeout):
        drive.wait_until_ready(timeout=2)

    # Attempt to catch any issues within the deconstruction and fail the test.
    try:
        del (drive)
    except:
        pytest.fail(traceback.format_exc())

    with pytest.raises(docker.errors.NotFound):
        docker.from_env().containers.get(id)


def test_image_removal():
    """ Test that we correctly remove the local image.

    This test ensures that a local downloaded image is deleted correctly if
    requested by the client. This feature allows the client to reduce the
    storage overhead of docker.
    """
    tag = "alpine:3.8"
    drive = driver.Driver(tag, remove_image=True)

    # Attempt to catch any issues within the deconstruction and fail the test.
    try:
        del (drive)
    except:
        pytest.fail(traceback.format_exc())

    assert not docker.from_env().images.list(tag)
