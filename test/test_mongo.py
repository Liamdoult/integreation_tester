import traceback

import pymongo
import pytest

from integration_tester import mongo_driver


def test_mongo():
    """ Standard MongoDB test. """
    drive = mongo_driver.MongoDBDriver()
    drive.wait_until_ready()

    db = pymongo.MongoClient().test
    collection = db.test
    collection.insert_one({"test": "test"})
    assert list(collection.find({}))

    drive.reset()
    assert not list(collection.find({}))

    # Attempt to catch any issues within the deconstruction and fail the test.
    try:
        del (drive)
    except:
        pytest.fail(traceback.format_exc())
