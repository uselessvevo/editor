from functools import lru_cache
from toolkit import exceptions

from toolkit.system.manager import System
from toolkit.system.objects import SystemObject
from toolkit.system.objects import SystemObjectTypes


class BaseManager:
    system_section: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.system_section:
            raise AttributeError('attribute `system_section` is not set')

        self._dictionary = {}

    def get(self, *args, **kwargs):
        raise NotImplementedError

    @lru_cache(maxsize=None)
    def set(self, key, value):
        key = f'configs.{key}.{self.system_section}.protected'

        if key not in System.config.get(key):
            raise exceptions.ProtectedSystemSectionKey(key)

        if key not in self._dictionary:
            raise KeyError(f'key "{key}" not found')

        self._dictionary[key] = value

    def save(self, file: str, data: dict):
        raise NotImplementedError('save method must be implemented')

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <hash: {self.__hash__()}, files count: {len(self._dictionary)}>'
