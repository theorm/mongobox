# -*- coding: utf-8 -*-

import os
import tempfile
import copy
import subprocess
import time
import sys
import shutil

from .utils import find_executable, get_free_port

MONGOD_BIN = 'mongod'
DEFAULT_ARGS = [
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
]
STARTUP_TIME = 0.4

class MongoBox(object):
    def __init__(self, mongod_bin=None, port=None, 
        log_path=None, db_path=None, scripting=False, 
        prealloc=False):

        self.mongod_bin = mongod_bin or find_executable(MONGOD_BIN)
        assert self.mongod_bin, 'Could not find "{}" in system PATH. Make sure you have MongoDB installed.'.format(MONGOD_BIN)

        self.port = port or get_free_port()
        self.log_path = log_path or os.devnull
        self.scripting = scripting
        self.prealloc = prealloc
        self.db_path = db_path

        if self.db_path:
            if os.path.exists(self.db_path) and os.path.isfile(self.db_path):
                raise AssertionError('DB path should be a directory, but it is a file.')

        self.process = None

    def start(self):
        if self.db_path:
            if not os.path.exists(self.db_path):
                os.mkdir(self.db_path)
            self._db_path_is_temporary = False
        else:
            self.db_path = tempfile.mkdtemp()
            self._db_path_is_temporary = True

        args = copy.copy(DEFAULT_ARGS)
        args.insert(0, self.mongod_bin)

        args.extend(['--dbpath', self.db_path])
        args.extend(['--port', str(self.port)])
        args.extend(['--logpath', self.log_path])

        if not self.scripting:
            args.append("--noscripting")

        if not self.prealloc:
            args.append("--noprealloc")

        self.process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        time.sleep(STARTUP_TIME)

    def stop(self):
        if not self.process:
            return

        if sys.platform == 'darwin':
            self.process.kill()
        else:
            self.process.terminate()
        self.process.wait()


        if self._db_path_is_temporary:
            shutil.rmtree(self.db_path)
            self.db_path = None

        self.process = None

    def running(self):
        return self.process is not None
