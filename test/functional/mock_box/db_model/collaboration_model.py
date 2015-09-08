# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # pylint:disable=redefined-builtin,wildcard-import,unused-wildcard-import
import sqlalchemy
import uuid
from test.functional.mock_box.db_model import DbModel


class CollaborationModel(DbModel):
    """DB Model for Box collaborations."""
    __tablename__ = 'box_collaboration'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    collab_id = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)
    item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_folder.id'))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime)
    modified_at = sqlalchemy.Column(sqlalchemy.DateTime)
    created_by_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
    status = sqlalchemy.Column(sqlalchemy.String(10))
