# coding: utf-8

from __future__ import unicode_literals, absolute_import
import json

from ..config import API
from ..session.box_session import BoxSession
from ..network.default_network import DefaultNetwork
from ..object.cloneable import Cloneable
from ..util.api_call_decorator import api_call
from ..object.search import Search
from ..object.events import Events
from ..util.shared_link import get_shared_link_header


class Client(Cloneable):

    def __init__(
            self,
            oauth=None,
            network_layer=None,
            session=None,
    ):
        """
        :param oauth:
            OAuth2 object used by the session to authorize requests.
        :type oauth:
            :class:`OAuth2`
        :param network_layer:
            The Network layer to use. If none is provided then an instance of :class:`DefaultNetwork` will be used.
        :type network_layer:
            :class:`Network`
        :param session:
            The session object to use. If None is provided then an instance of :class:`BoxSession` will be used.
        :type session:
            :class:`BoxSession`
        """
        super(Client, self).__init__()
        network_layer = network_layer or DefaultNetwork()
        self._oauth = oauth
        self._network = network_layer
        self._session = session or BoxSession(oauth=oauth, network_layer=network_layer)

    @api_call
    def make_request(self, method, url, **kwargs):
        """
        Make an authenticated request to the Box API.

        :param method:
            The HTTP verb to use for the request.
        :type method:
            `unicode`
        :param url:
            The URL for the request.
        :type url:
            `unicode`
        :return:
            The network response for the given request.
        :rtype:
            :class:`BoxResponse`
        :raises:
            :class:`BoxAPIException`
        """
        return self._session.request(method, url, **kwargs)
