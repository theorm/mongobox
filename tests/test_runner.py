import unittest
from mongorunner import MongoRunner, MultipleMongoRunner


class TestRunner(unittest.TestCase):

    def setUp(self):
        self.mongorunner = MongoRunner('testing')

    def test_runner(self):
        db = self.mongorunner.db_connection()
        collection = db['test']
        collection.save({'foo':'bar'})
        
        self.assertEquals(collection.find().count(), 1)
        
        self.assertTrue(self.mongorunner.db_name.startswith('testing')) 


class TestMultipleRunner(unittest.TestCase):

    def setUp(self):
        self.prefixes = ['one', 'two', 'three']
        self.mongorunner = MultipleMongoRunner(self.prefixes)

    def test_runner(self):
        dbs = self.mongorunner.db_connections()

        for prefix, db in zip(self.prefixes, dbs):
            print db.name
            self.assertTrue(db.name.startswith(prefix))