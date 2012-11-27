import unittest
from mongorunner import MongoRunner


class TestRunner(unittest.TestCase):

    def setUp(self):
        self.mongorunner = MongoRunner('testing')

    def test_runner(self):
        db = self.mongorunner.db_connection()
        collection = db['test']
        collection.save({'foo':'bar'})
        
        self.assertEquals(collection.find().count(), 1)
        
        self.assertTrue(self.mongorunner.db_name.startswith('testing')) 
