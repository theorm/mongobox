Mongo Box
---------

Mongo Box helps starting and stopping sandboxed MongoDB instance
from within a Python process. MongoDB instance is created with a
temporary directory to store database file and is configured to
be as lightweight as possible. It will choose a free port on localhost, 
so it will not interfere with default MongoDB processes. 
It is primarily expected to be used in unit tests and for prototyping concepts.

A typical use of a Mongo Box:

```python
from mongobox import MongoBox

box = MongoBox()
box.start()

client = box.client() # pymongo client 
assert client.alive()

# do stuff with Mongo

box.stop()
assert not client.alive()
```

Nose
----

Mongo Box comes with a Nose plugin which is automatically installed.
If used as a plugin, port of the running instance will be exported
in environment variable `MONGOBOX_PORT`. This name can be overridden
in settings.

The plugin exposes several configuration options. To see them, run:

    nosetests --help

The options you are interested in start with `--mongobox-`.

Unit tests
----------

For an easy unit tests integration there is a `MongoTestCase` class
inherited from `unittest.TestCase`. It assumes tests are run from `nosetests`
with `--with-mongobox` flag. `MongoTestCases` provides a `pymongo` client
connected to the sandboxed mongo instance and a `purge_database` helper
to clean up the database after every test:

```python
from mongobox.unittest import MongoTestCase

class MyTest(MongoTestCase):
    def setUp(self):
        deploy_fixtures(self.mongo_client)

    def tearDown(self):
        self.purge_database()
```

Installation
------------

Get it from PyPi:

    pip install mongobox

Get it from GitHub:
    
    pip install https://github.com/theorm/mongobox.git



Authors
=======

 Roman Kalyakin 


Thanks
------

MongoBox is based on `mongonose` nose plugin by Kapil Thangavelu.

For a list of contributors see `AUTHORS.md`.



