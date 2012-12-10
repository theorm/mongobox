#   Copyright 2011 Kapil Thangavelu
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from datetime import datetime
import pymongo

from nose.plugins import Plugin


def scan_path(executable="mongod"):
    """Scan the path for a binary.
    """
    for p in os.environ.get("PATH", "").split(":"):
        p = os.path.abspath(p)
        executable_path = os.path.join(p, executable)
        if os.path.exists(executable_path):
            return executable_path


def get_open_port(host="localhost"):
    """Get an open port on the machine.
    """
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temp_sock.bind((host, 0))
    port = temp_sock.getsockname()[1]
    temp_sock.close()
    del temp_sock
    return port


class MongoDBPlugin(Plugin):
    """A nose plugin that setups a test managed mongodb instance.
    """

    def __init__(self):
        super(MongoDBPlugin, self).__init__()
        self.mongodb_bin = None
        self.db_port = None
        self.db_path = None
        self.process = None
        self._running = False
        self._enabled = False
        self.name = 'mongorunner'

    def options(self, parser, env={}):
        parser.add_option(
            "--mongodb",
            action="store_true",
            default=False,
            help="Enable the mongodb plugin.")

        parser.add_option(
            "--mongodb-bin",
            dest="mongodb_bin",
            action="store",
            default=None,
            help="Optionally specify the path to the mongod executable.")

        parser.add_option(
            "--mongodb-port",
            action="store",
            dest="mongodb_port",
            type="int",
            default=0,
            help="Optionally specify the port to run mongodb on.")
        parser.add_option(
            "--mongodb-scripting",
            action="store_true",
            dest="mongodb_scripting",
            default=False,
            help="Optionally enables mongodb script engine.")
        parser.add_option(
            "--mongodb-logpath",
            action="store",
            dest="mongodb_logpath",
            default="/dev/null",
            help=("Optionally store the mongodb "
                  "log here (default is /dev/null)"))
        parser.add_option(
            "--mongodb-prealloc",
            action="store_true",
            dest="mongodb_prealloc",
            default=False,
            help=("Optionally preallocate db files"))

    def configure(self, options, conf):
        """Parse the command line options.
        """
        # This option has to be specified on the command line, to enable the
        # plugin.
        super(MongoDBPlugin, self).configure(options, conf)

        if not options.mongodb or options.mongodb_bin:
            return

        if not options.mongodb_bin:
            self.mongodb_bin = scan_path()
            if self.mongodb_bin is None:
                raise AssertionError(
                    "Mongodb plugin enabled, but no mongod on path, "
                    "please specify path to binary\n"
                    "ie. --mongodb=/path/to/mongod")
        else:
            self.mongodb_bin = os.path.abspath(
                os.path.expanduser(os.path.expandvars(options.mongodb_bin)))
            if not os.path.exists(self.mongodb_bin):
                raise AssertionError(
                    "Invalid mongodb binary %r" % self.mongodb_bin)

        self._enabled = True

        self.db_log_path = os.path.expandvars(os.path.expanduser(
            options.mongodb_logpath))
        try:
            fh = open(self.db_log_path, "w")
            fh.close()
        except Exception, e:
            raise AssertionError("Invalid log path %r" % e)

        if not options.mongodb_port:
            self.db_port = get_open_port()
        else:
            self.db_port = options.mongodb_port
        self.db_prealloc = options.mongodb_prealloc
        self.db_scripting = options.mongodb_scripting

    @property
    def enabled(self):
        return self._enabled

    def begin(self):
        """Start an instance of mongodb
        """

        if "TEST_MONGODB" in os.environ or self._running or not self._enabled:
            return

        # Stores data here
        self.db_path = tempfile.mkdtemp()
        if not os.path.exists(self.db_path):
            os.mkdir(self.db_path)

        args = [
            self.mongodb_bin,
            "--dbpath",
            self.db_path,
            "--port",
            str(self.db_port),
            # don't flood stdout, we're not reading it
            "--quiet",
            # save the port
            "--nohttpinterface",
            # disable unused.
            "--nounixsocket",
            # use a smaller default file size
            "--smallfiles",
            # journaling on by default in 2.0 and makes it to slow
            # for tests, can causes failures in jenkins
            "--nojournal",
            # Default is /dev/null
            "--logpath",
            self.db_log_path
            ]

        if not self.db_prealloc:
            args.append("--noprealloc")

        if not self.db_scripting:
            args.append("--noscripting")

        self.process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            )

        self._running = True
        os.environ["TEST_MONGODB"] = "localhost:%s" % self.db_port
        # Give a moment for mongodb to finish coming up
        time.sleep(0.3)

    def finalize(self, result):
        """Stop the mongodb instance.
        """
        if not self._running:
            return

        # Clear out the env variable.
        del os.environ["TEST_MONGODB"]

        # Kill the mongod process
        if sys.platform == 'darwin':
            self.process.kill()
        else:
            self.process.terminate()
        self.process.wait()

        # Clean out the test data.
        shutil.rmtree(self.db_path)
        self._running = False


class MongoRunner(object):
    '''Helper class that creates a test database suffixed with seconds after epoch
    to ensure uniquiness and shares a connection to it.
    '''

    def __init__(self, db_prefix='nosetests'):
        if 'TEST_MONGODB' not in os.environ:
            raise RuntimeError('You must run nose with --mongodb parameter to enable "mongonose" plugin. If you do not have it: $ pip install mongonose.')
        self._host, self._port = os.environ['TEST_MONGODB'].split(':')
        self._port = int(self._port)
        self.db_name = '{0}_{1}'.format(db_prefix, datetime.now().strftime('%s'))
        
        conn = pymongo.Connection(self._host, self._port)
        self._db = conn[self.db_name]

    def db_connection(self):
        return self._db

    def drop_database(self):
        self._db.connection.drop_database(self.db_name)


class MultipleMongoRunner(object):
    '''Helper class that creates a test database suffixed with seconds after epoch
    to ensure uniquiness and shares a connection to it.

    The difference from :class:`MongoRunner` is that you can specify several databases to be handled
    by one object in a sandboxed mongo instance.
    '''

    def __init__(self, db_prefixes=['nosetests']):
        if 'TEST_MONGODB' not in os.environ:
            raise RuntimeError('You must run nose with --mongodb parameter to enable "mongonose" plugin. If you do not have it: $ pip install mongonose.')
        self._host, self._port = os.environ['TEST_MONGODB'].split(':')
        self._port = int(self._port)

        self._connection = pymongo.Connection(self._host, self._port)

        self.db_names = []
        self._dbs = []
        timestamp = datetime.now().strftime('%s')
        for db_prefix in db_prefixes:
            db_name = '{0}_{1}'.format(db_prefix, timestamp)
            self.db_names.append(db_name) 

    def db_connections(self):
        return [self._connection[db_name] for db_name in self.db_names]

    def drop_databases(self):
        for db_name in self.db_names:
            self._connection.drop_database(db_name)
