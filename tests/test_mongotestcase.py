# -*- coding: utf-8 -*-
from mongobox.unittest import MongoTestCase


class MongoTestCaseTestCase(MongoTestCase):

    @classmethod
    def setUpClass(cls):
        # intentionally created class based method.
        pass

    def setUp(self):
        self.test_collection = self.mongo_client['test']['test']
        self.test_collection.insert_one({'foo': 'bar'})

    def tearDown(self):
        self.purge_database()

    def test_one_record(self):
        self.assertEqual(
            1, self.test_collection.count(),
            'Database expected to be purged in tearDown'
        )

    def test_one_record_once_again(self):
        self.assertEqual(
            1, self.test_collection.count(),
            'Database expected to be purged in tearDown'
        )
