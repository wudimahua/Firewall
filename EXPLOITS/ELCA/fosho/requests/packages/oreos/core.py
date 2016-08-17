# -*- coding: utf-8 -*-

"""
oreos.core
~~~~~~~~~~

The creamy white center.
"""

from .monkeys import SimpleCookie


def dict_from_string(s):
    ''''''


    cookies = dict()

    c = SimpleCookie()
    c.load(s)

    for k,v in c.items():
        cookies.update({k: v.value})

    return cookies