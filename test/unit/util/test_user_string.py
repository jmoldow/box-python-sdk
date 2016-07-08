# coding: utf-8

from __future__ import absolute_import, unicode_literals

import pytest
from six import text_type, PY2
from six.moves import UserString as PythonUserString

from boxsdk.util.user_string import UserString


TEXT_LIKE_OBJECTS = [u'foo', u'ƒøø', PythonUserString(u'foo')]
if PY2:
    TEXT_LIKE_OBJECTS.extend([b'foo', PythonUserString(b'foo')])
else:
    TEXT_LIKE_OBJECTS.append(PythonUserString(u'ƒøø'))  # This is broken on PY2 (which is why we created our UserString subclass).


BYTE_STRING_LIKE_OBJECTS = [u'ƒøø'.encode('utf-8')]
if PY2:
    BYTE_STRING_LIKE_OBJECTS.append(PythonUserString(u'ƒøø'.encode('utf-8')))
else:
    BYTE_STRING_LIKE_OBJECTS.append(b'foo')


@pytest.fixture(params=TEXT_LIKE_OBJECTS)
def text_like_object(request):
    return request.param


@pytest.fixture
def user_string(text_like_object):
    return UserString(text_like_object)


@pytest.fixture(params=[False, True])
def other_should_be_user_string(request):
    return request.param


@pytest.fixture(params=TEXT_LIKE_OBJECTS)
def other_text_like_object(request, other_should_be_user_string):
    if other_should_be_user_string:
        return UserString(request.param)
    return request.param


@pytest.fixture(params=BYTE_STRING_LIKE_OBJECTS)
def byte_string_like_object(request):
    return request.param


def test_init(user_string):
    pass


def test_init_rejects_byte_strings(byte_string_like_object):
    with pytest.raises(TypeError):
        UserString(byte_string_like_object)


def test_str(user_string, text_like_object):
    assert text_type(user_string) == text_type(text_like_object)


def test_repr(user_string):
    assert repr(user_string)


def test_add(user_string, text_like_object, other_text_like_object):
    concat = user_string + other_text_like_object
    assert isinstance(concat, UserString)
    assert concat == text_like_object + other_text_like_object


def test_add_rejects_byte_strings(user_string, byte_string_like_object):
    with pytest.raises(TypeError):
        user_string + byte_string_like_object


def test_radd(user_string, text_like_object, other_text_like_object):
    concat = other_text_like_object + user_string
    assert isinstance(concat, UserString)
    assert concat == other_text_like_object + text_like_object


def test_radd_rejects_byte_strings(user_string, byte_string_like_object):
    with pytest.raises(TypeError):
        byte_string_like_object + user_string
