# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import *
from enum import Enum
from six import text_type


class TextEnum(text_type, Enum):
    def __repr__(self):
        return self._value_  # pylint:disable=no-member

    def __str__(self):
        return str(self.value)  # pylint:disable=no-member
