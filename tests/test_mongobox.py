# -*- coding: utf-8 -*-
import unittest
import os
import tempfile
import shutil
from pymongo import MongoClient
from mongobox import MongoBox
from mongobox.nose_plugin import DEFAULT_PORT_ENVVAR


class TestMongoBox(unittest.TestCase):

    def test_nose_plugin_exports_envvar(self):
        self.assertTrue(DEFAULT_PORT_ENVVAR in os.environ)

    def test_can_run_mongo(self):
        box = MongoBox()
        box.start()

        self.assertTrue(box.running())
        self.assertIsNotNone(box.port)

        db_path = box.db_path

        client = MongoClient(port=box.port)
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
