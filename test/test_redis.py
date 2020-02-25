import traceback

import pytest
import redis

from integration_tester import redis_driver


def test_redis():
    """ Standard redis test. """
    drive = redis_driver.RedisDriver()
    drive.wait_until_ready(timeout=60)

    db = redis.Redis()
    assert db.set("test", "test")
    assert db.get("test").decode("utf-8") == "test"

    drive.reset()
    assert db.get("test") is None

    # Attempt to catch any issues within the deconstruction and fail the test.
    try:
        del (drive)
    except:
        pytest.fail(traceback.format_exc())
