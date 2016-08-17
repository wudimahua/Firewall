# -*- coding: utf-8 -*-

"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.

"""

import cgi
import codecs
import os
import random
import re
import zlib
from netrc import netrc, NetrcParseError

from .compat import parse_http_list as _parse_list_header
from .compat import quote, cookielib, SimpleCookie, is_py2, urlparse
from .compat import basestring, bytes, str


NETRC_FILES = ('.netrc', '_netrc')


def dict_to_sequence(d):
    ''''''


    if hasattr(d, 'items'):
        d = d.items()

    return d


def get_netrc_auth(url):
    ''''''


    locations = (os.path.expanduser('~/{0}'.format(f)) for f in NETRC_FILES)
    netrc_path = None

    for loc in locations:
        if os.path.exists(loc) and not netrc_path:
            netrc_path = loc

    ##

    if netrc_path is None:
        return netrc_path

    ri = urlparse(url)

    ##

    host = ri.netloc.split(':')[0]

    try:
        _netrc = netrc(netrc_path).authenticators(host)
        if _netrc:
            ##

            login_i = (0 if _netrc[0] else 1)
            return (_netrc[login_i], _netrc[2])
    except (NetrcParseError, IOError, AttributeError):
        ##

        ##

        pass


def dict_from_string(s):
    ''''''


    cookies = dict()

    try:
        c = SimpleCookie()
        c.load(s)

        for k, v in list(c.items()):
            cookies.update({k: v.value})
    ##

    except Exception:
        pass

    return cookies


def guess_filename(obj):
    ''''''

    name = getattr(obj, 'name', None)
    if name and name[0] != '<' and name[-1] != '>':
        return name


##

def parse_list_header(value):
    ''''''

    result = []
    for item in _parse_list_header(value):
        if item[:1] == item[-1:] == '"':
            item = unquote_header_value(item[1:-1])
        result.append(item)
    return result


##

def parse_dict_header(value):
    ''''''

    result = {}
    for item in _parse_list_header(value):
        if '=' not in item:
            result[item] = None
            continue
        name, value = item.split('=', 1)
        if value[:1] == value[-1:] == '"':
            value = unquote_header_value(value[1:-1])
        result[name] = value
    return result


##

def unquote_header_value(value, is_filename=False):
    ''''''

    if value and value[0] == value[-1] == '"':
        ##

        ##

        ##

        ##

        value = value[1:-1]

        ##

        ##

        ##

        ##

        ##

        if not is_filename or value[:2] != '\\\\':
            return value.replace('\\\\', '\\').replace('\\"', '"')
    return value


def header_expand(headers):
    ''''''


    collector = []

    if isinstance(headers, dict):
        headers = list(headers.items())
    elif isinstance(headers, basestring):
        return headers
    elif isinstance(headers, str):
        ##

        ##

        ##

        return headers.encode("latin-1")
    elif headers is None:
        return headers

    for i, (value, params) in enumerate(headers):

        _params = []

        for (p_k, p_v) in list(params.items()):

            _params.append('%s=%s' % (p_k, p_v))

        collector.append(value)
        collector.append('; ')

        if len(params):

            collector.append('; '.join(_params))

            if not len(headers) == i + 1:
                collector.append(', ')

    ##

    if collector[-1] in (', ', '; '):
        del collector[-1]

    return ''.join(collector)


def randombytes(n):
    ''''''

    if is_py2:
        L = [chr(random.randrange(0, 256)) for i in range(n)]
    else:
        L = [chr(random.randrange(0, 256)).encode('utf-8') for i in range(n)]
    return b"".join(L)


def dict_from_cookiejar(cj):
    ''''''


    cookie_dict = {}

    for _, cookies in list(cj._cookies.items()):
        for _, cookies in list(cookies.items()):
            for cookie in list(cookies.values()):
                ##

                cookie_dict[cookie.name] = cookie.value

    return cookie_dict


def cookiejar_from_dict(cookie_dict):
    ''''''


    ##

    if isinstance(cookie_dict, cookielib.CookieJar):
        return cookie_dict

    ##

    cj = cookielib.CookieJar()

    cj = add_dict_to_cookiejar(cj, cookie_dict)

    return cj


def add_dict_to_cookiejar(cj, cookie_dict):
    ''''''


    for k, v in list(cookie_dict.items()):

        cookie = cookielib.Cookie(
            version=0,
            name=k,
            value=v,
            port=None,
            port_specified=False,
            domain='',
            domain_specified=False,
            domain_initial_dot=False,
            path='/',
            path_specified=True,
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={'HttpOnly': None},
            rfc2109=False
        )

        ##

        cj.set_cookie(cookie)

    return cj


def get_encodings_from_content(content):
    ''''''


    charset_re = re.compile(r'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I)

    return charset_re.findall(content)


def get_encoding_from_headers(headers):
    ''''''


    content_type = headers.get('content-type')

    if not content_type:
        return None

    content_type, params = cgi.parse_header(content_type)

    if 'charset' in params:
        return params['charset'].strip("'\"")

    if 'text' in content_type:
        return 'ISO-8859-1'


def stream_decode_response_unicode(iterator, r):
    ''''''


    if r.encoding is None:
        for item in iterator:
            yield item
        return

    decoder = codecs.getincrementaldecoder(r.encoding)(errors='replace')
    for chunk in iterator:
        rv = decoder.decode(chunk)
        if rv:
            yield rv
    rv = decoder.decode('', final=True)
    if rv:
        yield rv


def get_unicode_from_response(r):
    ''''''


    tried_encodings = []

    ##

    encoding = get_encoding_from_headers(r.headers)

    if encoding:
        try:
            return str(r.content, encoding)
        except UnicodeError:
            tried_encodings.append(encoding)

    ##

    try:
        return str(r.content, encoding, errors='replace')
    except TypeError:
        return r.content


def stream_decompress(iterator, mode='gzip'):
    ''''''


    if mode not in ['gzip', 'deflate']:
        raise ValueError('stream_decompress mode must be gzip or deflate')

    zlib_mode = 16 + zlib.MAX_WBITS if mode == 'gzip' else -zlib.MAX_WBITS
    dec = zlib.decompressobj(zlib_mode)
    try:
        for chunk in iterator:
            rv = dec.decompress(chunk)
            if rv:
                yield rv
    except zlib.error:
        ##

        yield chunk
        ##

        for chunk in iterator:
            yield chunk
    else:
        ##

        buf = dec.decompress(bytes())
        rv = buf + dec.flush()
        if rv:
            yield rv


def stream_untransfer(gen, resp):
    if 'gzip' in resp.headers.get('content-encoding', ''):
        gen = stream_decompress(gen, mode='gzip')
    elif 'deflate' in resp.headers.get('content-encoding', ''):
        gen = stream_decompress(gen, mode='deflate')

    return gen


##

UNRESERVED_SET = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    + "0123456789-._~")


def unquote_unreserved(uri):
    ''''''

    parts = uri.split('%')
    for i in range(1, len(parts)):
        h = parts[i][0:2]
        if len(h) == 2:
            c = chr(int(h, 16))
            if c in UNRESERVED_SET:
                parts[i] = c + parts[i][2:]
            else:
                parts[i] = '%' + parts[i]
        else:
            parts[i] = '%' + parts[i]
    return ''.join(parts)


def requote_uri(uri):
    ''''''

    ##

    ##

    ##

    return quote(unquote_unreserved(uri), safe="!#$%&'()*+,/:;=?@[]~")
