# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *

from .base_object import BaseObject


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'
