import pytest
import redis

from integration_tester import redis_driver 


def test_redis():
    """ Standard redis test. """
    database = redis_driver.RedisDriver()
    database.wait_until_ready(timeout=60)

    db = redis.Redis()
    assert db.set("test", "test")
    assert db.get("test").decode("utf-8") == "test"

    database.reset()
    assert db.get("test") is None
