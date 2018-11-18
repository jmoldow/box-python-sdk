# coding: utf-8

from __future__ import absolute_import, division, unicode_literals

from datetime import timedelta

from .str_repr import str_repr
from .types import CompatObject, CompatType, CompatObjectWithCompatType


__all__ = list(map(str, ['total_seconds', 'str_repr', 'CompatObject', 'CompatType', 'CompatObjectWithCompatType']))


if not hasattr(timedelta, 'total_seconds'):
    def total_seconds(delta):
        """
        Return the total number of seconds represented by this timedelta.
        Python 2.6 does not define this method.
        """
        return (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10 ** 6) / 10 ** 6
else:
    def total_seconds(delta):
        return delta.total_seconds()
