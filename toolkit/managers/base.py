from dotty_dict import dotty
from functools import lru_cache

from toolkit import exceptions
from toolkit.managers import System


class BaseManager:

    _dictionary = dotty({})
    _system_section = None

    def __init__(self, *args, **kwargs):
        if not self._system_section:
            raise NotImplementedError

    @lru_cache(maxsize=None)
    def get(self, key, default=None):
        return self._dictionary._data.get(key, default)

    @lru_cache(maxsize=None)
    def set(self, key, value):
        if key not in System.config.get(f'{key}.{self._system_section}.protected'):
            raise exceptions.ProtectedSystemSectionKey()

        if key not in self._dictionary:
            raise KeyError

        self._dictionary[key] = value

    def __repr__(self):
        return f'({self.__class__.__name__}) <hash: {self.__hash__()}, files count: {len(self._dictionary)}>'
