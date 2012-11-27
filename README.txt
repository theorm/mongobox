Mongo Db Nose Plugin
--------------------

A nose plugin that automates the creation and teardown of a mongodb
instance as part of test runs.

It's based on mongonose by Kapil Thangavelu with added support for 
latest version of nose and a MongoRunner helper class.

Installation
============

Grab the package off github::

    pip install  https://github.com/theorm/mongorunner/zipball/master

Its automatically picked up via entry points as a nose plugin.

Usage
=====

The plugin extends the nose options with a few options. The only
required options are either `--mongodb` or `--mongodb-bin` to enable
the plugin.

 - `--mongodb` is required to enable the mongodb plugin. 

 - `--mongodb-bin` Allows specifying the path to the `mongod` binary.
   If not specified the plugin will search the path for a mongodb
   binary. If one is not found, an error will be raised.

 - `--mongodb-port` can be optionally set, by default the plugin
   will utilize a a random open port on the machine.

 - `--mongodb-scripting` Enables the javascript scripting engine,
   off by default.

 - `--mongodb-logpath` Stores the server log at the given path, by
   default sent to /dev/null

 - `--mongodb-prealloc` Enables pre-allocation of databases, default
   is off. Modern filesystems will sparsely allocate, which can
   speed up test execution.

The plugin will populate the environment variable "TEST_MONGODB" which
contains the location to the mongodb server in ``host:port`` format.

Tests should use this environment variable value when connecting to mongodb.

Authors
=======

 Roman Kalyakin 





