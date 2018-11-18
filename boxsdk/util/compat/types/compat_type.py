# coding: utf-8

from __future__ import absolute_import, unicode_literals

import six

from .compat_object import CompatObject
from ..str_repr import str_repr


class CompatType(type, CompatObject):
    def __new__(metacls, *args, **kwargs):
        return str_repr(super(CompatType, metacls).__new__(metacls, *args, **kwargs))
