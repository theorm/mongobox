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
    import pymongo
    from mongobox import MongoBox

    box = MongoBox()
    box.start()

    client = pymongo.MongoClient(port=box.port) 
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

Installation
------------

Get it from GitHub:
    
    pip install https://github.com/theorm/mongobox


Thanks
------

MongoBox is based on `mongonose` nose plugin by Kapil Thangavelu.

Authors
=======

 Roman Kalyakin 





