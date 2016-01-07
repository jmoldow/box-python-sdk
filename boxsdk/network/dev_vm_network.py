# coding: utf-8

from __future__ import absolute_import, unicode_literals

from six.moves.urllib.parse import urljoin

from .custom_api_urls_network import CustomAPIURLsDefaultNetwork
from ..auth.oauth2 import OAuth2
from ..client import Client
from ..session.box_session import BoxSession


def dev_vm_api_urls(dev_vm_name):
    dev_vm_netloc = dev_vm_name + '.dev.box.net/'
    box_homepage = 'https://' + dev_vm_netloc
    return {
        'BASE_API_URL': urljoin(box_homepage, 'api/2.0'),
        'UPLOAD_URL': urljoin('https://upload.' + dev_vm_name + '.inside-box.net', 'api/2.0'),  # not .dev.box.net
        'OAUTH2_API_URL': urljoin(box_homepage, 'api/oauth2'),
        'OAUTH2_AUTHORIZE_URL': urljoin(box_homepage, 'api/oauth2/authorize'),
    }


class LiveOrDevVMNetwork(CustomAPIURLsDefaultNetwork):
    def __init__(self, dev_vm_name=None):
        if dev_vm_name:
            api_urls = dev_vm_api_urls(dev_vm_name)
        else:
            api_urls = {}   # Don't change any URLs, point at Live API.
        super(LiveOrDevVMNetwork, self).__init__(api_urls=api_urls)


class LiveOrDevVMOAuth2(OAuth2):
    def __init__(self, *args, **kwargs):
        network_layer = kwargs.pop('network_layer', None)
        dev_vm_name = kwargs.pop('dev_vm_name', None)
        network_layer = network_layer or LiveOrDevVMNetwork(dev_vm_name=dev_vm_name)
        if dev_vm_name and not args:
            kwargs.setdefault('client_id', '76sr7r935k2wsnlwokepg4tuaujz45p7')
            kwargs.setdefault('client_secret', 'VMLVGOOXjI8TsAjMt1INsXrqjoA5niL7')
        super(LiveOrDevVMOAuth2, self).__init__(*args, network_layer=network_layer, **kwargs)

class OAuthClient(Client):
    def __init__(self, oauth):
        super(OAuthClient, self).__init__(oauth=oauth, network_layer=oauth._network_layer)

class BoxOAuthSession(BoxSession):
    def __init__(self, oauth):
        super(BoxOAuthSession, self).__init__(oauth=oauth, network_layer=oauth._network_layer)
