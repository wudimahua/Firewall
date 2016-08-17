# -*- coding: utf-8 -*-

"""
requests.async
~~~~~~~~~~~~~~

This module contains an asynchronous replica of ``requests.api``, powered
by gevent. All API methods return a ``Request`` instance (as opposed to
``Response``). A list of requests can be sent with ``map()``.
"""

try:
    import gevent
    from gevent import monkey as curious_george
    from gevent.pool import Pool
except ImportError:
    raise RuntimeError('Gevent is required for requests.async.')

##

curious_george.patch_all(thread=False, select=False)

from . import api


__all__ = (
    'map', 'imap',
    'get', 'options', 'head', 'post', 'put', 'patch', 'delete', 'request'
)


def patched(f):
    ''''''


    def wrapped(*args, **kwargs):

        kwargs['return_response'] = False
        kwargs['prefetch'] = True

        config = kwargs.get('config', {})
        config.update(safe_mode=True)

        kwargs['config'] = config

        return f(*args, **kwargs)

    return wrapped


def send(r, pool=None, prefetch=False):
    ''''''


    if pool != None:
        return pool.spawn(r.send, prefetch=prefetch)

    return gevent.spawn(r.send, prefetch=prefetch)


##

get = patched(api.get)
options = patched(api.options)
head = patched(api.head)
post = patched(api.post)
put = patched(api.put)
patch = patched(api.patch)
delete = patched(api.delete)
request = patched(api.request)


def map(requests, prefetch=True, size=None):
    ''''''


    requests = list(requests)

    pool = Pool(size) if size else None
    jobs = [send(r, pool, prefetch=prefetch) for r in requests]
    gevent.joinall(jobs)

    return [r.response for r in requests]


def imap(requests, prefetch=True, size=2):
    ''''''


    pool = Pool(size)

    def send(r):
        r.send(prefetch)
        return r.response

    for r in pool.imap_unordered(send, requests):
        yield r

    pool.join()