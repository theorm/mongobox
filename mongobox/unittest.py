# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
import os

try:
    import pymongo
except ImportError:
    raise ImportError('PyMongo is required for MongoTestCase')


class MongoTestCase(TestCase):
    '''A base for Mongo DB driven test cases. Provides
    :class:`pymongo.MongoClient` instance in :attribute:`mongo_client`
    and has a :method:`purge_database` helper method for database cleanup.

    It is expected that tests are run from `nose` with `--with-mongobox` flag
    that brings up a sandboxed instance of Mongo.
    '''
    __mongo_client = None

    @property
    def mongo_client(self):
        '''Returns an instance of :class:`pymongo.MongoClient` connected
        to MongoBox database instance.
        '''
        if not self.__mongo_client:
            try:
                port = int(os.getenv('MONGOBOX_PORT'))
                self.__mongo_client = pymongo.MongoClient(port=port)
            except (TypeError, pymongo.errors.ConnectionFailure):
                raise RuntimeError(
                    'Seems that MongoBox is not running. ' +
                    'Do you run nosetests with --with-mongobox flag?')

        return self.__mongo_client

    def purge_database(self, drop=True):
        '''Drops all collections in all databases but system ones
        (``system.*``) one by one if :param:`drop` is `True` (default),
        otherwise removes documents using `remove` method.
        Both seem to be faster than dropping databases directly.

        A typical use is call this method in :func:`unittest.TestCase.tearDown`
        to have a clean database for every test case method.

        .. code-block:: python

        def tearDown(self):
            super(self, MyTestCase).tearDown()
            self.purge_database()
        '''
        for db_name in self.mongo_client.database_names():
            db = self.mongo_client[db_name]
            collections = [
                db[c] for c in db.collection_names()
                if not c.startswith('system.')
            ]
            for collection in collections:
                if drop:
                    db.drop_collection(collection)
                else:
                    collection.remove(None)
