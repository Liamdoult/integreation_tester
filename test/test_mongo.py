import pymongo 
import pytest

from integration_tester import mongo_driver


def test_mongo():
    """ Standard MongoDB test. """
    database = mongo_driver.MongoDBDriver()
    database.wait_until_ready()
    
    db = pymongo.MongoClient().test
    collection = db.test
    collection.insert_one({"test": "test"})
    assert list(collection.find({}))

    database.reset()
    assert not list(collection.find({}))
