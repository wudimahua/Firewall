''''''

import os
from threading import Lock
_counter_lock = Lock()

_counter = 0
def _get_next_counter():
    global _counter
    with _counter_lock:
        _counter += 1
        return _counter

_prefix = None

def choose_boundary():
    ''''''


    global _prefix
    import time
    if _prefix is None:
        import socket
        try:
            hostid = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            hostid = '127.0.0.1'
        try:
            uid = repr(os.getuid())
        except AttributeError:
            uid = '1'
        try:
            pid = repr(os.getpid())
        except AttributeError:
            pid = '1'
        _prefix = hostid + '.' + uid + '.' + pid
    return "%s.%.3f.%d" % (_prefix, time.time(), _get_next_counter())
