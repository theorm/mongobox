# -*- coding: utf-8 -*-
import unittest
import os
import tempfile
import shutil
from mongobox import MongoBox
from mongobox.nose_plugin import DEFAULT_PORT_ENVVAR
from pymongo.errors import OperationFailure

class TestMongoBox(unittest.TestCase):

    def test_nose_plugin_exports_envvar(self):
        self.assertTrue(DEFAULT_PORT_ENVVAR in os.environ)

    def test_can_run_mongo(self):
        box = MongoBox()
        box.start()

        db_path = box.db_path

        self.assertTrue(box.running())
        self.assertIsNotNone(box.port)

        client = box.client()
        self.assertTrue(client.alive())

        box.stop()
        
        self.assertFalse(box.running())
        self.assertFalse(client.alive())
        self.assertFalse(os.path.exists(db_path))


    def test_keep_db_path(self):
        db_path = tempfile.mkdtemp()
        box = MongoBox(db_path=db_path)
        box.start()
        box.stop()

        self.assertTrue(os.path.exists(db_path))
        shutil.rmtree(db_path)

    def test_auth(self):
        box = MongoBox(auth=True)
        box.start()
        
        client = box.client()
        client['admin'].add_user('foo','bar')
        self.assertRaises(OperationFailure, client['test'].add_user, 'test','test')
        client['admin'].authenticate('foo', 'bar')
        try:
            client['test'].add_user('test','test')
        except OperationFailure:
            self.fail("add_user() operation unexpectedly failed")
        
        client = box.client()
        self.assertRaises(OperationFailure, client['test'].collection_names)
        client['admin'].authenticate('foo', 'bar')
        try:
            client['test'].collection_names()
        except OperationFailure:
            self.fail("collection_names() operation unexpectedly failed")
        