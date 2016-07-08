# coding: utf-8

from __future__ import absolute_import, unicode_literals

from functools import wraps

from six import binary_type, text_type, PY2
from six.moves import UserString as PythonUserString


__all__ = [str('UserString')]


def _cast_argument_to_text(byte_string_type_error):
    def decorator(method):

        @wraps(method)
        def wrapper(self, text_like_object):
            if isinstance(text_like_object, PythonUserString):
                text_like_object = text_like_object.data
            if isinstance(text_like_object, binary_type):
                if PY2:
                    # Since Python 2 often considers `str` to be a text type,
                    # treat ascii-decodable `str` objects as text strings
                    # instead of byte strings.
                    try:
                        text_like_object = text_like_object.decode('ascii')
                    except UnicodeDecodeError:
                        raise type_error
                else:
                    raise type_error
            text = text_type(text_like_object)
            return method(self, text)

        return wrapper

    return decorator


_concat_type_error = TypeError(str("can't concat byte strings to text strings"))
_cast_concat_argument_to_text = _cast_argument_to_text(_concat_type_error)


# Acts more like a "UserText" / "UserUnicode", instead of a "UserBytes".
@wraps(PythonUserString, assigned=('__doc__',), updated=())
class UserString(PythonUserString):
    __slots__ = ()

    ## Methods that need to be modified to operate with text / unicode, instead of bytes.

    @_cast_argument_to_text(TypeError(str("argument can't be byte string")))
    def __init__(self, seq):
        super(UserString, self).__init__(seq)

    @_cast_concat_argument_to_text
    def __add__(self, other): return super(UserString, self).__add__(other)

    @_cast_concat_argument_to_text
    def __radd__(self, other): return super(UserString, self).__radd__(other)

    def __unicode__(self): return text_type(self.data)
