# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # pylint:disable=redefined-builtin,wildcard-import,unused-wildcard-import

from enum import Enum as _Enum

from future.utils import PY2, text_to_native_str as n


if PY2:
    class Enum(object, _Enum):
        pass
else:
    Enum = _Enum

__all__ = [n('Enum')]
