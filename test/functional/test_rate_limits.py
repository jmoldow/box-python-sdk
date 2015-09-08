# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *


def test_too_many_requests_causes_retry(box_client, mock_box, monkeypatch):
    monkeypatch.setattr(mock_box, 'RATE_LIMIT_THRESHOLD', 1)
    box_client.folder('0').get()
    box_client.folder('0').get()
    assert len(mock_box.requests) == 6  # 3 auth requests, 2 real requests, and a retry
