# coding: utf-8

from __future__ import unicode_literals
from aplus import Promise
from calendar import timegm
from contextlib import contextmanager
from betamax import Betamax
from bottle import Bottle, run, request, server_names, ServerAdapter
from datetime import datetime
from functools import partial
from mock import mock_open, patch
import os
import pytest
import re
import requests
import six
from six.moves.urllib import parse  # pylint:disable=import-error, no-name-in-module
import sys
from threading import Thread
import webbrowser
from boxsdk.auth.oauth2 import OAuth2
from boxsdk.config import API
from boxsdk.client import Client


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def box_client(box_oauth):
    # pylint:disable=redefined-outer-name
    return Client(box_oauth)


@pytest.fixture(scope='session')
def root_folder(box_client):
    return box_client.folder('0')


@pytest.yield_fixture(scope='function')
def test_root_folder(root_folder, betamax_recorder):
    folder_name = 'box-python-sdk-{time}'.format(time=timegm(datetime.utcnow().utctimetuple()))
    with betamax_recorder.use_cassette('test_root_folder', record='once'):#, match_requests_on=['method', 'uri', 'headers', 'query']):
        folder = root_folder.create_subfolder(folder_name)
        yield folder
        folder.delete()


@pytest.fixture(scope='session')
def oauth2(client_id, client_secret):
    # pylint:disable=redefined-outer-name
    return OAuth2(client_id, client_secret, box_device_name='python-box-sdk functional test')


@pytest.fixture(scope='session')
def box_oauth(oauth2, user_login, betamax_recorder):
    # pylint:disable=redefined-outer-name
    try:
        with betamax_recorder.use_cassette('box_oauth2', record='none'):
            return _authenticate(oauth2, user_login, dry_run=True)
    except ValueError:
        with betamax_recorder.use_cassette('box_oauth2', record='once'):
            return _authenticate(oauth2, user_login)


@pytest.fixture(scope='session')
def betamax_recorder(oauth2):
    # pylint:disable=redefined-outer-name
    with Betamax.configure() as conf:
        conf.preserve_exact_body_bytes = False
    return Betamax(
        oauth2.session,
        cassette_library_dir=os.path.join(here, 'vcr', 'cassettes'),
        #default_cassette_options={'match_requests_on': ['method', 'uri', 'headers', 'query']},
    )


@pytest.fixture(params=[
    'foo.txt',
    'bar.docx',
    'foo.txt',
])
def file_name(request):
    return request.param


@pytest.fixture(params=[
    'some_folder',
    'Ѵȁćȁƭȉőń Ρȉćƭȕŕȅŝ',
])
def folder_name(request):
    return request.param


@pytest.fixture(scope='session')
def user_name():
    return 'User 1'


@pytest.fixture(scope='session')
def user_login():
    # NOTE(jmoldow): In order for betamax to work, this needs to be a real user
    # login email address.
    return 'user.1@example.com'


@pytest.fixture()
def uploaded_file(test_root_folder, test_file_path, test_file_content, file_name):
    # pylint:disable=redefined-outer-name
    with patch('boxsdk.object.folder.open', mock_open(read_data=test_file_content), create=True):
        return test_root_folder.upload(test_file_path, file_name)


@pytest.fixture()
def created_subfolder(test_root_folder, folder_name):
    # pylint:disable=redefined-outer-name
    return test_root_folder.create_subfolder(folder_name)


bottle_server = None


def _authenticate(oauth2, user_login, dry_run=False):
    auth_code_result = Promise()
    # NOTE(jmoldow): In order for betamax to work, these need to be paths to an
    # RSA private key self-signed SSL certificate.
    cert_file = None
    pkey_file = None

    @contextmanager
    def run_bottle_server():
        #run local http server on a separate thread
        class SSLWSGIRefServer(ServerAdapter):
            def run(self, handler):
                import ssl
                from wsgiref.simple_server import WSGIRequestHandler, make_server
                global bottle_server
                if False and self.quiet:
                    class QuietHandler(WSGIRequestHandler):
                        def log_request(*args, **kw):
                            # pylint:disable=no-method-argument
                            pass
                    self.options['handler_class'] = QuietHandler
                srv = make_server(self.host, self.port, handler, **self.options)
                # pylint:disable=protected-access
                bottle_server = srv
                # pylint:enable=protected-access
                srv.socket = ssl.wrap_socket(srv.socket, certfile=cert_file, keyfile=pkey_file, server_side=True)
                f.flush()
                srv.serve_forever()
        server_names['ssl_server'] = SSLWSGIRefServer

        app = Bottle()

        @app.get('/')
        def get_token():
            # pylint:disable=unused-variable
            d = {'auth_code': request.query.code, 'state': request.query.state}
            f.flush()
            if hasattr(request.query, 'code'):
                auth_code_result.fulfill(d)
                return '<script>window.close();</script>'

        server_thread = Thread(target=partial(run, app, server=SSLWSGIRefServer(host='0.0.0.0', port=8080)))
        server_thread.start()

        yield
        bottle_server.shutdown()

    if dry_run:
        access_token, _ = oauth2.authenticate('')
    else:
        with run_bottle_server():
            generated_auth_url, csrf_token = oauth2.get_authorization_url('https://localhost:8080', box_login=user_login)
            webbrowser.open(generated_auth_url)
            #wait until the auth code is available
            auth_code = auth_code_result.get()
        assert auth_code['state'] == csrf_token
        access_token, _ = oauth2.authenticate(auth_code['auth_code'])
    access_token = access_token.rstrip()
    #return access_token
    return oauth2
