# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # pylint:disable=redefined-builtin,wildcard-import,unused-wildcard-import

from future.utils import with_metaclass

from boxsdk.util.singleton import Singleton


class Translator(with_metaclass(Singleton, object)):
    """
    Translate item responses from the Box API to Box objects.
    """
    def __init__(self):
        self._type_to_class_mapping = {}

    def register(self, type_name, box_cls):
        """
        Associate a Box object class to handle Box API item responses with the given type name.

        :param type_name:
            The type name to be registered.
        :type type_name:
            `unicode`
        :param box_cls:
            The Box object class, which will be associated with the type name provided.
        :type box_cls:
            `type`
        """
        self._type_to_class_mapping.update({
            type_name: box_cls,
        })

    def translate(self, type_name):
        """
        Get the box object class associated with the given type name.

        :param type_name:
            The type name to be translated.
        :type type_name:
            `unicode`
        """
        from boxsdk.object.base_object import BaseObject
        return self._type_to_class_mapping.get(type_name, BaseObject)
