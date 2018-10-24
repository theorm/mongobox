# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess
import time
import sys
import shutil
import socket

from .utils import find_executable, get_free_port

is_windows = lambda: sys.platform.startswith("win")

MONGOD_BIN = 'mongod.exe' if is_windows() else 'mongod'
DEFAULT_ARGS = [
    # don't flood stdout, we're not reading it
    "--quiet",
    # disable unused.
    "--nounixsocket",
    # use a smaller default file size
    "--smallfiles",
    # journaling on by default in 2.0 and makes it to slow
    # for tests, can causes failures in jenkins
    "--nojournal",
]
STARTUP_TIME = 0.4
START_CHECK_ATTEMPTS = 200


class MongoBox(object):
    def __init__(self, mongod_bin=None, port=None,
                 db_path=None, scripting=False,
                 prealloc=False, auth=False, storage_engine=None):

        if db_path and os.path.exists(db_path) and os.path.isfile(db_path):
            raise AssertionError('DB path should be a directory, but it is a file.')

        self.mongod_bin = mongod_bin or find_executable(MONGOD_BIN)

        self.port = port or get_free_port()
        self.scripting = scripting
        self.prealloc = prealloc
        self.db_path = db_path
        self._db_path_is_temporary = not self.db_path
        self.auth = auth
        self.storage_engine = storage_engine

        self.process = None

    def start(self):
        """Start MongoDB.
        """
        if self._db_path_is_temporary:
            self.db_path = tempfile.mkdtemp()
        elif not os.path.exists(self.db_path):
            os.mkdir(self.db_path)

        args = [self.mongod_bin] + list(DEFAULT_ARGS)

        args.extend(['--dbpath', self.db_path])
        args.extend(['--port', str(self.port)])

        self.log_path = os.path.join(self.db_path, 'mongodb.log')
        args.extend(['--logpath', self.log_path])

        if self.storage_engine:
            args.extend(['--storageEngine', self.storage_engine])

        if self.auth:
            args.append("--auth")

        if not self.scripting:
            args.append("--noscripting")

        if not self.prealloc:
            args.append("--noprealloc")

        self.process_args = args

        self.fnull = open(os.devnull, 'w')
        self.process = subprocess.Popen(args, stdout=self.fnull, stderr=subprocess.STDOUT)

        self._wait_till_started()

    def _wait_till_started(self):
        attempts = 0
        while True:
            if self.process.poll() is not None:  # the process has terminated
                with open(self.log_path) as log_file:
                    raise SystemExit('MondgoDB failed to start:\n{}\n{}'.format(
                        ' '.join(self.process_args), log_file.read()))
            attempts += 1
            if attempts > START_CHECK_ATTEMPTS:
                break
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                try:
                    s.connect(('localhost', int(self.port)))
                    return
                except (IOError, socket.error):
                    time.sleep(0.25)
            finally:
                s.close()

        # MongoDB still does not accept connections. Killing it.
        self.stop()

    def stop(self):
        if self.process is None or self.process.poll() is not None:
            # the process does not exist anymore
            return
        
        # Not sure if there should be more checks for
        # other platforms.
        if sys.platform == 'darwin':
            self.process.kill()
        elif is_windows():
            self.process.terminate()
        else:
            os.kill(self.process.pid, 9)
        self.process.wait()

        if self._db_path_is_temporary:
            shutil.rmtree(self.db_path)
            self.db_path = None

        self.process = None
        self.fnull.close()
        self.fnull = None

    def running(self):
        return self.process is not None

    def client(self):
        import pymongo
        try:
            return pymongo.MongoClient(port=self.port)  # version >=2.4
        except AttributeError:
            return pymongo.Connection(port=self.port)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
