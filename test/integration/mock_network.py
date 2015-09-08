# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # pylint:disable=redefined-builtin,wildcard-import,unused-wildcard-import
from mock import Mock
import requests
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.network.network_interface import Network


class MockNetwork(Network):
    """Mock implementation of the network interface for testing purposes."""

    def __init__(self):
        super(MockNetwork, self).__init__()
        self._session = Mock(requests.Session)
        self._retries = []

    def request(self, method, url, access_token, **kwargs):
        """Base class override.
        Make a mock network request using a mock requests.Session.
        """
        return DefaultNetworkResponse(self._session.request(method, url, **kwargs), access_token)

    def retry_after(self, delay, request_method, *args, **kwargs):
        """Base class override.
        Retry immediately, recording the retry request.
        """
        self._retries.append((delay, request_method, args, kwargs))
        return request_method(*args, **kwargs)

    @property
    def session(self):
        return self._session
