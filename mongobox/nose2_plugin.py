"""
nose2.cfg should contain:

    [unittest]
    plugins = mongobox.nose2_plugin

    [mongobox]
    # Optionally specify the path to the mongod executable
    # bin =
    # Optionally specify the port to run mongodb on
    # port =
    # Optionally enables mongodb script engine
    # scripting = True
    # Path to database files directory. Creates temporary directory by default
    # dbpath =
    # Optionally store the mongodb log here (default is /dev/null)
    # logpath =
    # Optionally preallocate db files
    # prealloc = True
    # Specify storage engine to use
    # https://docs.mongodb.org/manual/release-notes/3.2-compatibility/#default-storage-engine-change
    # storage_engine =
    # Which environment variable port number will be exported to
    port_envvar = MONGOBOX_PORT

"""
import logging
import os

import nose2.events

from .mongobox import MongoBox


log = logging.getLogger('nose2.plugins.mongobox')


DEFAULT_PORT_ENVVAR = 'MONGOBOX_PORT'


class MongoBoxPlugin(nose2.events.Plugin):
    """A nose plugin that setups a sandboxed mongodb instance.
    """
    configSection = 'mongobox'

    def __init__(self):
        self.register()  # always on
        self.mongobox = MongoBox(
            mongod_bin=self.config.get('bin'),
            port=self.config.as_int('port'),
            db_path=self.config.get('dbpath'),
            scripting=self.config.as_bool('scripting', False),
            prealloc=self.config.as_bool('prealloc', False),
            storage_engine=self.config.get('storage_engine'),
        )
        self.port_envvar = self.config.get('port_envvar', DEFAULT_PORT_ENVVAR)

    def pluginsLoaded(self, event):
        # start MongoDB server here before the tests and the tested application are imported
        # because some apps connect to MongoDB during import
        assert self.port_envvar not in os.environ, (
            '{} environment variable is already taken. '
            'Do you have other tests with mongobox running?'.format(self.port_envvar))

        self.mongobox.start()
        os.environ[self.port_envvar] = str(self.mongobox.port)

    def afterTestRun(self, event):
        self.mongobox.stop()
        del os.environ[self.port_envvar]
