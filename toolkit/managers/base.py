from functools import lru_cache
from toolkit import exceptions

from toolkit.managers.system.manager import System
from toolkit.managers.system.objects import SystemObject


class BaseManager(SystemObject):

    def __init__(self):
        self._dictionary = {}
        super().__init__()

    def get(self, *args, **kwargs):
        raise NotImplementedError('Method "get" must be implemented')

    def save(self, file: str, data: dict):
        raise NotImplementedError('Method "save" must be implemented')

    @lru_cache(maxsize=None)
    def set(self, key, value):
        key = f'configs.{key}.{self.section}.protected'

        if key not in System.config.get(key):
            raise exceptions.ProtectedSystemSectionKey(key)

        if key not in self._dictionary:
            raise KeyError(f'key "{key}" not found')

        self._dictionary[key] = value

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)
