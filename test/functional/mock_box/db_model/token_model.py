# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import sqlalchemy
import uuid
from test.functional.mock_box.db_model import DbModel


class TokenModel(DbModel):
    """DB Model for Box tokens."""
    __tablename__ = 'box_token'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    owned_by_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
    authorized_application_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_application.id'))
    expires_at = sqlalchemy.Column(sqlalchemy.DateTime)
    token_type = sqlalchemy.Column(sqlalchemy.Enum('access', 'refresh'), nullable=False)
    token = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)
