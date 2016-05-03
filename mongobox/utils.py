# -*- coding: utf-8 -*-
import os
import socket


def find_executable(executable):
    """Scan PATH for an executable.
    """
    for path in os.environ.get('PATH', '').split(os.pathsep):
        path = os.path.abspath(path)
        executable_path = os.path.join(path, executable)
        if os.path.isfile(executable_path):
            return executable_path

    raise AssertionError('Could not find "{}" in system PATH. Make sure you have it installed.'.format(
        executable))


def get_free_port(host="localhost"):
    """Get a free port on the machine.
    """
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temp_sock.bind((host, 0))
    port = temp_sock.getsockname()[1]
    temp_sock.close()
    del temp_sock
    return port
