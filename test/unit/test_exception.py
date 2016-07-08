# coding: utf-8

from __future__ import unicode_literals

import pytest
import re
from rotunicode import ruencode
from six import text_type, PY2
from six.moves import map

from boxsdk.exception import BoxException, BoxAPIException, BoxNetworkException, BoxOAuthException
from boxsdk.util.text import encode, decode

@pytest.fixture(scope='module', params=[str, unicode] if PY2 else [str])
def string_type(request):
    return request.param

@pytest.fixture(scope='module', params=[BoxException, BoxNetworkException])
def standard_box_exception_class(request):
    return request.param

@pytest.fixture(scope='module', params=[BoxAPIException, BoxOAuthException])
def box_api_exception_class(request):
    return request.param

@pytest.fixture(scope='module', params=[
    (),
    (ruencode('foo'),),
    (ruencode('foo'), ruencode('bar')),
    (ruencode('foo'), 200, ruencode('bar')),
])
def exception_args(request):
    return tuple(map(encode, request.param))

@pytest.fixture(scope='module', params=[
    {},
    {'message': ruencode('foobarbaz')},
    {'message': ruencode('foobarbaz'), 'method': 'GET'},
    {'message': ruencode('foobarbaz'), 'method': 'GET', 'url': 'https://{0}.com'.format(ruencode('example'))},
])
def exception_kwargs(request):
    return request.param

def test_box_exception_string(standard_box_exception_class, exception_args, string_type):
    expected_text = str(Exception(*exception_args))
    if PY2 and string_type is unicode:
        expected_text = decode(expected_text)
    assert string_type(standard_box_exception_class(*exception_args)) == expected_text

def test_box_exception_repr(standard_box_exception_class, exception_args):
    class_name = standard_box_exception_class.__name__
    expected_text = re.sub(r',\)$', r')', repr(Exception(*exception_args)).replace('Exception', class_name))
    assert repr(standard_box_exception_class(*exception_args)) == expected_text

def test_box_api_exception_repr(box_api_exception_class):
    message = ruencode('foobarbaz')
    url = 'https://{0}.com'.format(ruencode('example'))
    exception_kwargs = {'message': message, 'method': 'GET', 'url': url}
    message = repr(message)
    url = repr(url)
    get = repr('GET')
    class_name = box_api_exception_class.__name__
    expected_repr = encode("{class_name}(400, message={message}, method={get}, url={url})".format(**locals()))
    assert repr(box_api_exception_class(400, **exception_kwargs)) == expected_repr

def test_box_api_exception():
    status = 400
    code = 'code'
    message = ruencode('message')
    request_id = 12345
    headers = {'header': 'value'}
    url = 'https://{0}.com'.format(ruencode('example'))
    method = 'GET'
    context_info = {'context': ruencode('value')}
    box_exception = BoxAPIException(
        status,
        code=code,
        message=message,
        request_id=request_id,
        headers=headers,
        url=url,
        method=method,
        context_info=context_info,
    )
    assert box_exception.status == status
    assert box_exception.code == code
    assert box_exception.message == message
    assert box_exception.request_id == request_id
    assert box_exception._headers == headers  # pylint:disable=protected-access
    assert box_exception.url == url
    assert box_exception.method == method
    assert box_exception.context_info == context_info
    assert text_type(box_exception) == '''
Message: {0}
Status: {1}
Code: {2}
Request id: {3}
Headers: {4}
URL: {5}
Method: {6}
Context info: {7}'''.format(message, status, code, request_id, headers, url, method, context_info)


def test_box_oauth_exception():
    status = 400
    message = ruencode('message')
    url = 'https://{0}.com'.format(ruencode('message'))
    method = 'GET'
    box_exception = BoxOAuthException(
        status,
        message=message,
        url=url,
        method=method,
    )
    assert text_type(box_exception) == '''
Message: {0}
Status: {1}
URL: {2}
Method: {3}'''.format(message, status, url, method)
