# coding: utf-8

from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractproperty

from six import add_metaclass, binary_type, text_type


@add_metaclass(ABCMeta)
class RangesSpecifier(object):
    @abstractproperty
    def range_unit(self):
        """
        :return:
        :rtype:
            `bytes`
        """
        raise NotImplementedError

    @abstractproperty
    def range_set(self):
        """
        :return:
        :rtype:
            `bytes`
        """
        raise NotImplementedError

    def __bytes__(self):
        return binary_type(b'{self.range_unit}={self.range_set}'.format(self=self))

    def __str__(self):
        return str(self.__bytes__())

    def __unicode__(self):
        return unicode(str(self))

    def __repr__(self):
        return str(str('{self.__class__.__name__}({self})').format(self=self))
