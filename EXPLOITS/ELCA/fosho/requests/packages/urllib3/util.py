# urllib3/util.py
##

##

##

##



from base64 import b64encode

try:
    from select import poll, POLLIN
except ImportError: ##

    poll = False
    try:
        from select import select
    except ImportError: ##

        select = False

from .packages import six
from .exceptions import LocationParseError


def make_headers(keep_alive=None, accept_encoding=None, user_agent=None,
                 basic_auth=None):
    ''''''

    headers = {}
    if accept_encoding:
        if isinstance(accept_encoding, str):
            pass
        elif isinstance(accept_encoding, list):
            accept_encoding = ','.join(accept_encoding)
        else:
            accept_encoding = 'gzip,deflate'
        headers['accept-encoding'] = accept_encoding

    if user_agent:
        headers['user-agent'] = user_agent

    if keep_alive:
        headers['connection'] = 'keep-alive'

    if basic_auth:
        headers['authorization'] = 'Basic ' +            b64encode(six.b(basic_auth)).decode('utf-8')

    return headers


def get_host(url):
    ''''''


    ##

    ##

    port = None
    scheme = 'http'

    if '://' in url:
        scheme, url = url.split('://', 1)
    if '/' in url:
        url, _path = url.split('/', 1)
    if '@' in url:
        _auth, url = url.split('@', 1)
    if ':' in url:
        url, port = url.split(':', 1)

        if not port.isdigit():
            raise LocationParseError("Failed to parse: %s" % url)

        port = int(port)

    return scheme, url, port



def is_connection_dropped(conn):
    ''''''

    sock = getattr(conn, 'sock', False)
    if not sock: ##

        return False

    if not poll: ##

        if not select: ##

            return False

        return select([sock], [], [], 0.0)[0]

    ##

    p = poll()
    p.register(sock, POLLIN)
    for (fno, ev) in p.poll(0.0):
        if fno == sock.fileno():
            ##

            return True
