# coding: utf-8

from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod
from types import NoneType

from six import add_metaclass, binary_type, integer_types

from .ranges_specifier import RangesSpecifier


class ByteRangesSpecifier(RangesSpecifier):
    def __init__(self, byte_range_set):
        super(ByteRangesSpecifier, self).__init__()
        self._byte_range_set = byte_range_set

    @property
    def range_unit(self):
        return b'bytes'

    @property
    def range_set(self):
        return binary_type(self.byte_range_set)

    @property
    def byte_range_set(self):
        return self._byte_range_set


class ByteRangeSet(list):
    def __init__(self, iterable):
        super(ByteRangeSet, self).__init__(iterable)
        if not self:
            raise TypeError('{self.__class__.__name__}.__init__() takes a non-empty iterable'.format(self=self))
        for item in self:
            if not isinstance(item, ByteRange):
                message = "{self.__class__.__name__}.__init__() takes an iterable of ByteRange, but got an item of type '{item.__class__.__name__}'"
                raise TypeError(message.format(self=self, item=item))

    def __bytes__(self):
        return binary_type(b','.join(map(binary_type, self)))

    def __str__(self):
        return str(self.__bytes__())

    def __unicode__(self):
        return unicode(str(self))

    def __repr__(self):
        return str('{self.__class__.__name__}({byte_range_set})'.format(self=self, byte_range_set=super(ByteRangeSet, self).__repr__()))


@add_metaclass(ABCMeta)
class ByteRange(object):
    @abstractmethod
    def __bytes__(self):
        raise NotImplementedError

    def __str__(self):
        return str(self.__bytes__())

    def __unicode__(self):
        return unicode(str(self))

    def __repr__(self):
        return str(str('{self.__class__.__name__}({self})').format(self=self))


class ByteRangeSpecifier(ByteRange):
    def __init__(self, first_byte_position_inclusive, **kwargs):
        _int_message = '__init__(): first_byte_position_inclusive must be an int, got {actual_type}'
        _int_or_none_message = '__init__(): {parameter_name} must be an int or None, got {actual_type}'
        _wrong_number_message = '__init__() takes exactly 3 arguments ({given} given)'
        if not isinstance(first_byte_position_inclusive, integer_types):
            raise TypeError(_int_message.format(actual_type=first_byte_position_inclusive.__class__.__name__))
        self._first_byte_position = first_byte_position_inclusive
        if 'last_byte_position_inclusive' in kwargs:
            last_byte_position_inclusive = kwargs.pop('last_byte_position_inclusive')
            if not isinstance(last_byte_position_inclusive, (integer_types, NoneType)):
                raise TypeError(_int_or_none_message.format(parameter_name='last_byte_position_inclusive', actual_type=last_byte_position_inclusive.__class__.__name__))
        elif 'last_byte_position_exclusive' in kwargs:
            last_byte_position_exclusive = kwargs.pop('last_byte_position_exclusive')
            if not isinstance(last_byte_position_exclusive, (integer_types, NoneType)):
                raise TypeError(_int_or_none_message.format(parameter_name='last_byte_position_exclusive', actual_type=last_byte_position_exclusive.__class__.__name__))
            last_byte_position_inclusive = last_byte_position_exclusive - 1
        else:
            raise TypeError(_wrong_number_message.format(given=2))
        self._last_byte_position = last_byte_position_inclusive
        if kwargs:
            raise TypeError(_wrong_number_message.format(given=(3 + len(kwargs))))
        super(ByteRangeSpecifier, self).__init__()

    @property
    def first_byte_position_inclusive(self):
        return self._first_byte_position

    @property
    def last_byte_position_inclusive(self):
        return self._last_byte_position

    @property
    def last_byte_position_exclusive(self):
        return (self._last_byte_position + 1) if self._last_byte_position else None

    @property
    def _last_byte_position_inclusive_bytes(self):
        return binary_type(self.last_byte_position_inclusive) or b''

    def __bytes__(self):
        return b'{self.first_byte_position}-{self._last_byte_position_inclusive_bytes}'.format(self=self)


class SuffixByteRangeSpecifier(ByteRange):
    def __init__(self, suffix_length):
        if not isinstance(suffix_length, integer_types):
            raise TypeError('suffix_length must be an int, got {actual_type}'.format(actual_type=suffix_length.__class__.__name__))
        self._suffix_length = suffix_length
        super(SuffixByteRangeSpecifier, self).__init__()

    @property
    def suffix_length(self):
        return self._suffix_length

    def __bytes__(self):
        return b'-{self.suffix_length}'
