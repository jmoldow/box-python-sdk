# coding: utf-8

from __future__ import absolute_import, unicode_literals

__doc__ = (
"""RFC 7230 utilities.

RFC 7230
Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing

<https://datatracker.ietf.org/doc/rfc7230/>

Defines various compiled regular expressions for patterns in the RFC 7230
grammar.
"""
)

import re


__all__ = list(map(str, [
    'OPTIONAL_WHITESPACE_PATTERN', 'BAD_WHITESPACE_PATTERN',
    'TOKEN_CHARACTER_PATTERN', 'TOKEN_PATTERN',
    'DOUBLE_QUOTED_STRING_START_CHARACTER',
]))


# DQUOTE
_DOUBLE_QUOTE_CHARACTER = b'"'

# SP / HTAB
_SPACE_OR_HORIZONTAL_TAB_CHARACTER_PATTERN = re.compile(rb"[ \t]")


###########################################################
#   <https://tools.ietf.org/html/rfc7230#section-3.2.3>   #
###########################################################

# OWS
OPTIONAL_WHITESPACE_PATTERN = re.compile(_SPACE_OR_HORIZONTAL_TAB_CHARACTER_PATTERN.pattern + rb"*")

# BWS
BAD_WHITESPACE_PATTERN = OPTIONAL_WHITESPACE_PATTERN


###########################################################
#   <https://tools.ietf.org/html/rfc7230#section-3.2.6>   #
###########################################################

# tchar
TOKEN_CHARACTER_PATTERN = re.compile(rb"[!#$%&'*+\-.^_`|~0-9a-zA-Z]")

# token
TOKEN_PATTERN = re.compile(TOKEN_CHARACTER_PATTERN.pattern + rb"+")

# quoted-string start character
DOUBLE_QUOTED_STRING_START_CHARACTER = _DOUBLE_QUOTE_CHARACTER
