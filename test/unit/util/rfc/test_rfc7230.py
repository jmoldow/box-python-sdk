# coding: utf-8

from __future__ import absolute_import, unicode_literals

import re

import pytest
import six

from boxsdk.util.rfc import rfc7230


REPattern = re.compile(r"").__class__

TOKEN_CHARACTERS = list(b"! # $ % & ' * + - . ^ _ ` | ~ 0 9 a z A Z".split(b" "))
NOT_TOKEN_CHARACTERS = list(rb'" ( ) , / : ; < = > ? @ [ \ ] { }'.split(b" "))


@pytest.fixture(params=list(range(4)))
def spaces(request):
    return (b" " * request.param)


@pytest.fixture(params=list(range(4)))
def horizontal_tabs(request):
    return (b"\t" * request.param)


@pytest.fixture
def whitespace(horizontal_tabs, spaces):
    return horizontal_tabs + spaces


@pytest.fixture(params=TOKEN_CHARACTERS)
def token_character(request):
    return request.param


@pytest.fixture(params=NOT_TOKEN_CHARACTERS)
def not_token_character(request):
    return request.param


@pytest.fixture(params=list(range(2)))
def start_position(request):
    return request.param


@pytest.fixture(params=list(range(1, 3)))
def length(request):
    return request.param


@pytest.fixture
def token(token_character, start_position, length):
    return token_character + token_character.join(TOKEN_CHARACTERS[start_position:(start_position + length)])


def test_OPTIONAL_WHITESPACE_PATTERN():
    assert isinstance(rfc7230.OPTIONAL_WHITESPACE_PATTERN, REPattern)


def test_OPTIONAL_WHITESPACE_PATTERN_positive_match(whitespace):
    match = rfc7230.OPTIONAL_WHITESPACE_PATTERN.match(whitespace + b"/")
    assert match
    assert match.group() == whitespace


def test_BAD_WHITESPACE_PATTERN():
    assert rfc7230.BAD_WHITESPACE_PATTERN is rfc7230.OPTIONAL_WHITESPACE_PATTERN


def test_TOKEN_CHARACTER_PATTERN():
    assert isinstance(rfc7230.TOKEN_CHARACTER_PATTERN, REPattern)


def test_TOKEN_CHARACTER_PATTERN_positive_match(token_character):
    match = rfc7230.TOKEN_CHARACTER_PATTERN.match(token_character)
    assert match
    assert match.group() == token_character


def test_TOKEN_CHARACTER_PATTERN_only_matches_one_character(token_character):
    match = rfc7230.TOKEN_CHARACTER_PATTERN.match(token_character * 2)
    assert match
    assert match.group() == token_character


def test_TOKEN_CHARACTER_PATTERN_does_not_match_empty_string():
    assert not rfc7230.TOKEN_CHARACTER_PATTERN.search(b"")


def test_TOKEN_CHARACTER_PATTERN_no_match(not_token_character):
    assert not rfc7230.TOKEN_CHARACTER_PATTERN.search(not_token_character)


def test_TOKEN_PATTERN():
    assert isinstance(rfc7230.TOKEN_PATTERN, REPattern)


def test_TOKEN_PATTERN_positive_match(token):
    match = rfc7230.TOKEN_PATTERN.match(token)
    assert match
    assert match.group() == token


def test_TOKEN_PATTERN_does_not_match_empty_string():
    assert not rfc7230.TOKEN_PATTERN.search(b"")


def test_TOKEN_PATTERN_no_match(not_token_character):
    assert not rfc7230.TOKEN_PATTERN.search(not_token_character * 2)


def test_DOUBLE_QUOTED_STRING_START_CHARACTER():
    assert isinstance(rfc7230.DOUBLE_QUOTED_STRING_START_CHARACTER, six.binary_type)
    assert rfc7230.DOUBLE_QUOTED_STRING_START_CHARACTER == b'"'
