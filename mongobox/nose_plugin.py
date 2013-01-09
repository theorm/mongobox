# -*- coding: utf-8 -*-
from nose.plugins import Plugin
from .mongobox import MongoBox
import os

DEFAULT_PORT_ENVVAR = 'MONGOBOX_PORT'

class MongoBoxPlugin(Plugin):
    """A nose plugin that setups a sandboxed mongodb instance.
    """
    name = 'mongobox'

    def options(self, parser, env):
        super(MongoBoxPlugin, self).options(parser, env)
        parser.add_option(
            "--mongobox-bin",
            dest="bin",
            action="store",
            default=None,
            help="Optionally specify the path to the mongod executable.")
        parser.add_option(
            "--mongobox-port",
            action="store",
            dest="port",
            type="int",
            default=0,
            help="Optionally specify the port to run mongodb on.")
        parser.add_option(
            "--mongobox-scripting",
            action="store_true",
            dest="scripting",
            default=False,
            help="Optionally enables mongodb script engine.")
        parser.add_option(
            "--mongobox-dbpath",
            action="store",
            dest="dbpath",
            default=None,
            help=("Path to database files directory. Creates temporary directory by default."))
        parser.add_option(
            "--mongobox-logpath",
            action="store",
            dest="logpath",
            default=None,
            help=("Optionally store the mongodb log here (default is /dev/null)"))
        parser.add_option(
            "--mongobox-prealloc",
            action="store_true",
            dest="prealloc",
            default=False,
            help=("Optionally preallocate db files"))
        parser.add_option(
            "--mongobox-port-envvar",
            action="store",
            dest="port_envvar",
            default=DEFAULT_PORT_ENVVAR,
            help="Which environment variable dynamic port number will be exported to.")


    def configure(self, options, conf):
        super(MongoBoxPlugin, self).configure(options, conf)

        self.mongobox = MongoBox(mongod_bin=options.bin, port=options.port or None,
                log_path=options.logpath, db_path=options.dbpath, 
                scripting=options.scripting, prealloc=options.prealloc)

        self.port_envvar = options.port_envvar

    def begin(self):
        assert self.port_envvar not in os.environ, '{} environment variable is already taken. Do you have other tests with mongobox running?'.format(self.port_envvar)
        
        self.mongobox.start()
        os.environ[self.port_envvar] = str(self.mongobox.port)

    def finalize(self, result):
        self.mongobox.stop()
        del os.environ[self.port_envvar]
