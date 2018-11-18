# coding: utf-8

from __future__ import absolute_import, unicode_literals

import six

from ..str_repr import str_repr


def func(unbound_method):
    return getattr(unbound_method, '__func__', unbound_method)


@str_repr
class CompatObject(object):
    def __bool__(self):
        super_object = super(CompatObject, self)
        try:
            super_bool = super_object.__bool__
        except AttributeError:
            pass
        else:
            return super_bool()

        if (func(self.__class__.__nonzero__) is func(CompatObject.__nonzero__)) and (not hasattr(super_object, '__nonzero__')):
            return True

        return self.__nonzero__()

    def __nonzero__(self):
        super_object = super(CompatObject, self)
        try:
            super_nonzero = super_object.__nonzero__
        except AttributeError:
            pass
        else:
            return super_nonzero()

        if (func(self.__class__.__bool__) is func(CompatObject.__bool__)) and (not hasattr(super_object, '__bool__')):
            return True

        return self.__bool__()

    def __unicode__(self):
        try:
            super_unicode = super(CompatObject, self).__unicode__
        except AttributeError:
            return self.__str__()
        return super_unicode()

    def __str__(self):
        super_str = super(CompatObject, self).__str__
        if super_str == object.__str__.__get__(self, self.__class__):
