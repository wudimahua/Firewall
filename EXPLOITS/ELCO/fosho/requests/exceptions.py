# -*- coding: utf-8 -*-

"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests' exceptions.

"""

class RequestException(RuntimeError):
    ''''''


class HTTPError(RequestException):
    ''''''

    response = None

class ConnectionError(RequestException):
    ''''''


class SSLError(ConnectionError):
    ''''''


class Timeout(RequestException):
    ''''''


class URLRequired(RequestException):
    ''''''


class TooManyRedirects(RequestException):
    ''''''


class MissingSchema(RequestException, ValueError):
    ''''''


class InvalidSchema(RequestException, ValueError):
    ''''''
