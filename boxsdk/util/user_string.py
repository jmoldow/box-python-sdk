# coding: utf-8

from __future__ import absolute_import, unicode_literals

from six import text_type, PY2
from six.moves import UserString as PythonUserString


__all__ = [str(b'UserString')]


if PY2:

    # Acts more like a "UserText" / "UserUnicode", instead of a "UserBytes".
    class UserString(PythonUserString):
        __doc__ = PythonUserString.__doc__
        __slots__ = ()

        ## Methods that need to be modified to operate with text / unicode, instead of bytes.

        def __init__(self, seq):
            super(UserString, self).__init__(self._to_text(seq))

        def __unicode__(self): return unicode(self.data)

        def __add__(self, other): return super(UserString, self).__add__(self._to_text(other))

        def __radd__(self, other): return super(UserString, self).__radd__(self._to_text(other))

        ## Helper

        def _to_text(self, obj):
            """Convert object to a text/unicode-like object.

            :type obj: `object`
            :rtype: :class:`UserString` or `unicode`
            """
            if isinstance(obj, (text_type, UserString)):
                return obj
            return text_type(obj)

else:
    UserString = PythonUserString
