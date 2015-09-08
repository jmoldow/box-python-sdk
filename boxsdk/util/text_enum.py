# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # pylint:disable=redefined-builtin,wildcard-import,unused-wildcard-import

from enum import EnumMeta

from future.utils import PY2, with_metaclass
from future.types.newstr import BaseNewStr

from .enum import Enum


if PY2:
    class TextEnumMeta(BaseNewStr, EnumMeta):
        pass
else:
    TextEnumMeta = EnumMeta


class TextEnum(with_metaclass(TextEnumMeta, str, Enum)):
    pass
