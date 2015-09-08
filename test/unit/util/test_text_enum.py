# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import *
from boxsdk.util.text_enum import TextEnum


class MockTextEnum(TextEnum):
    member = 'member'


def test_text_enum_repr_is_value():
    assert MockTextEnum.member.__repr__() == MockTextEnum.member.value  # pylint:disable=no-member


def test_text_enum_str_is_value():
    assert str(MockTextEnum.member) == str('member')
