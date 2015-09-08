# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object


class API(object):
    """Configuration object containing the URLs for the Box API."""
    BASE_API_URL = 'https://api.box.com/2.0'
    UPLOAD_URL = 'https://upload.box.com/api/2.0'
    OAUTH2_API_URL = 'https://api.box.com/oauth2'  # <https://developers.box.com/docs/#oauth-2>
    OAUTH2_AUTHORIZE_URL = 'https://app.box.com/api/oauth2/authorize'  # <https://developers.box.com/docs/#oauth-2-authorize>
