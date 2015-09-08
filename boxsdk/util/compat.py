# coding: utf-8

from __future__ import division, unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # pylint:disable=redefined-builtin,wildcard-import,unused-wildcard-import


from datetime import timedelta

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
