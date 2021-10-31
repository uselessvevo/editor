import types
import typing

from toolkit import exceptions
from functools import lru_cache
from toolkit.managers.system.manager import System


class ManagerMixin:
    _dictionary: typing.Dict = {}

    @lru_cache(maxsize=None)
    def set(self, key, value) -> None:
        key = f'{key}.{self.section}.{self.config_access.value}'

        if key not in System.config.get(key):
            raise exceptions.ProtectedSystemSectionKey(key)

        if key not in self._dictionary:
            raise KeyError(f'key "{key}" not found')

        self._dictionary[key] = value

    def __call__(self, *args, **kwargs) -> typing.Any:
        return self.get(*args, **kwargs)
