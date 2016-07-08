# coding: utf-8

from __future__ import absolute_import, unicode_literals

import pytest
from six import text_type, PY2
from six.moves import UserString as PythonUserString

from boxsdk.util.user_string import UserString


TEXT_LIKE_OBJECTS = set([u'foo', u'ƒøø', str(b'foo'), PythonUserString(b'foo')])


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


def test_init(user_string):
    pass


def test_str(user_string, text_like_object):
    assert text_type(user_string) == text_type(text_like_object)


def test_repr(user_string):
    assert repr(user_string)


def test_add(user_string, text_like_object, other_text_like_object):
    assert user_string + other_text_like_object == text_like_object + other_text_like_object


def test_radd(user_string, text_like_object, other_text_like_object):
    assert other_text_like_object + user_string == other_text_like_object + text_like_object
