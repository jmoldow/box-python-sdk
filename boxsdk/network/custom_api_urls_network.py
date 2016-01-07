# coding: utf-8

from __future__ import absolute_import, unicode_literals

from .default_network import DefaultNetwork
from .network_interface import Network


__all__ = list(map(str, ['CustomAPIURLsNetwork', 'CustomAPIURLsDefaultNetwork']))


class CustomAPIURLsNetwork(Network):
    """
    Mixin that dynamically creates a `Network.API` subclass with custom URLs.
    """

    def __init__(self, api_urls, **kwargs):
        """
        :param api_urls:
            The dictionary of attributes to use when created the
            :class:`Network.API` subclass. Keys should be some or all of the
            constant class attributes of :class:`NetworkAPI`, and values should
            be URLs.
        :type api_urls:
            `dict` of `str` to `unicode`
        """
        super(CustomAPIURLsNetwork, self).__init__(**kwargs)
        self._API = self._construct_API_subclass_from_urls(api_urls)

    @property
    def API(self):
        """Return a subclass of `Network.API`, which redefines some or all of its constant class attributes.

        :return:
            A subclass of :class:`Network.API`.
        :type:
            `type`
        """
        return self._API

    @staticmethod
    def _construct_API_subclass_from_urls(api_urls, name=str('CustomAPI'), API=None):
        API = API or Network.API
        return type(name, (API,), api_urls)


class CustomAPIURLsDefaultNetwork(CustomAPIURLsNetwork, DefaultNetwork):
    pass
