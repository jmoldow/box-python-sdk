# coding: utf-8

from __future__ import absolute_import, unicode_literals

import functools

import six


def str_repr(cls):
    if six.PY2:
        cls_repr = cls.__repr__

        @functools.wraps(cls_repr, assigned=('__doc__',), updated=())
        def __repr__(self):
            repr_str = cls_repr(self)
            if isinstance(repr_str, six.text_type):
                return repr_str.encode('utf-8')
            return repr_str

        try:
            functools.update_wrapper(__repr__, cls_repr, assigned=('__module__',), updated=('__dict__',))
        except AttributeError:
            pass

        cls.__repr__ = __repr__
    return cls
