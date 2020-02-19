from integration_tester import driver, errors

import docker
import pytest 


def test_driver_standard():
    """ Standard driver use test. """
    tag = "ubuntu:latest"
    drive = driver.Driver(tag)
    id = drive._container.id
    assert drive.ready() == True
    assert drive.reset() is None 
    assert drive.wait_until_ready(timeout=10) is None
    drive._status = False 
    with pytest.raises(errors.ReadyTimeout):
        drive.wait_until_ready(timeout=2)
    del(drive)
    with pytest.raises(docker.errors.NotFound):
        driver.CLIENT.containers.get(id)
    

def test_image_removal():
    """ Test that we correctly remove the local image.

    This test ensures that a local downloaded image is deleted correctly if
    requested by the client. This feature allows the client to reduce the
    storage overhead of docker.
    """
    tag = "alpine:3.8"
    drive = driver.Driver(tag, remove_image=True)
    del(drive)
    assert not driver.CLIENT.images.list(tag)