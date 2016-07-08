# coding: utf-8

from __future__ import unicode_literals

from six import PY2

if PY2:
    string_types = [str, unicode]
    def encode(obj): return obj.encode('utf-8') if isinstance(obj, unicode) else obj
    def decode(obj): return obj.decode('utf-8') if isinstance(obj, str) else obj
else:
    string_types = [str]
    def encode(obj): return obj
    def decode(obj): return obj
