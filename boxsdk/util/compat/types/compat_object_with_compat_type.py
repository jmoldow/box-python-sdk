# coding: utf-8

from __future__ import absolute_import, unicode_literals

import six

from .compat_object import CompatObject
from .compat_type import CompatType


class CompatObjectWithCompatType(six.with_metaclass(CompatType, CompatObject)):
    pass
