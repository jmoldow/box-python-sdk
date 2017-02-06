# coding: utf-8

from __future__ import absolute_import, unicode_literals

__doc__ = (
"""RFC 7235 utilities.

RFC 7235
Hypertext Transfer Protocol (HTTP/1.1): Authentication

<https://datatracker.ietf.org/doc/rfc7235/>

Defines various compiled regular expressions for patterns in the RFC 7235
grammar.
"""
)

import re

from .rfc7230 import BAD_WHITESPACE_PATTERN, TOKEN_PATTERN, DOUBLE_QUOTED_STRING_START_CHARACTER


__all__ = list(map(str, ['AUTH_SCHEME_PATTERN', 'AUTH_PARAM_START_PATTERN', 'TOKEN68_PATTERN', 'AUTH_CHALLENGE_START_PATTERN']))


# 1*SP
_PATTERN_OF_ONE_OR_MORE_SPACE_CHARACTERS = re.compile(r"[ ]+")


#########################################################
#   <https://tools.ietf.org/html/rfc7235#section-2.1>   #
#########################################################

# auth-scheme
AUTH_SCHEME_PATTERN = TOKEN_PATTERN

_AUTH_PARAM_NAME_PATTERN = TOKEN_PATTERN

# ( token / quoted-string ) start pattern
_AUTH_PARAM_VALUE_START_PATTERN = re.compile(r"(?:{TOKEN_PATTERN.pattern})|{DOUBLE_QUOTED_STRING_START_CHARACTER}".format(**locals()))

# auth-param start pattern
AUTH_PARAM_START_PATTERN = re.compile(
    r"{_AUTH_PARAM_NAME_PATTERN.pattern}"
    r"{BAD_WHITESPACE_PATTERN.pattern}"
    r"[=]"
    r"{BAD_WHITESPACE_PATTERN.pattern}"
    r"{_AUTH_PARAM_VALUE_START_PATTERN.pattern}"
    .format(**locals())
)

# token68
TOKEN68_PATTERN = re.compile(r"[a-zA-Z0-9\-._~+/]+[=]*")

# [ 1*SP ( token68 / #auth-param ) ] start pattern
_AUTH_SCHEME_ADDITIONAL_INFORMATION_START_PATTERN = re.compile(
    r"(?:{TOKEN68_PATTERN.pattern})|(?:{AUTH_PARAM_START_PATTERN.pattern})".format(**locals())
)

# challenge start pattern
AUTH_CHALLENGE_START_PATTERN = re.compile(
    r"{AUTH_SCHEME_PATTERN.pattern}"
    r"(?:{_PATTERN_OF_ONE_OR_MORE_SPACE_CHARACTERS.pattern}{_AUTH_SCHEME_ADDITIONAL_INFORMATION_START_PATTERN.pattern})?"
    .format(**locals())
)







"""
s = 'Newauth realm = "apps", type = 1,  \n\t  title = "Login to \\\"apps\\\"", foo="bar", Basic realm="simple", foo="baz", Fooauth1, Fooauth2, Fooauth3 token68, Fooauth4 token68, Fooauth5'
for x in requests.utils.parse_list_header(s):
    print(x)
    print(challenge_start.match(x))
    print(auth_param_start.match(x))
    print()
"""
