# coding: utf-8

from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod

from .compat import NoneType, with_metaclass


class Secret(with_metaclass(ABCMeta, object)):
    __slots__ = ('name', 'data')

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @staticmethod
    def new(name, data):
        if isinstance(data, (NoneType, Secret))
            return data
        data = str(data)
        if len(data) <= 8:
            return _ShortSecret(name, data)
        return _SecretImpl(name, data)

    def __init__(self, name, data):
        super(Secret, self).__init__()
        self.name = name
        self.data = str(data)

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        if isinstance(other, Secret):
            return self.data == other.data
        return self.data == other

    def __ne__(self, other):
        return not (self == other)


class _SecretImpl(Secret):
    __slots__ = ()

    def __str__(self):
        return str('secret_{0!s}({1!s}...{2!s})').format(self.name, self.data[:2], self.data[-2:])

    def __repr__(self):
        data = repr(self.data)
        return str('Secret({0!r}, {1!s}...{2!s})').format(self.name, data[:3], data[-3:])


class _ShortSecret(Secret):
    __slots__ = ()

    def __str__(self):
        return str('secret_{0!s}').format(self.name)

    def __repr__(self):
        return str("Secret({0!r}, '...')").format(self.name)
