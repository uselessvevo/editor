from pathlib import Path

from toolkit.managers.system.objects import SystemObject, SystemObjectTypes
from toolkit.utils.files import read_json
from toolkit.utils.files import write_json

from toolkit.managers.system.manager import System
from toolkit.managers.base import BaseManager
from toolkit.utils.os import get_locale


class LocalesManager(BaseManager):
    name = 'translation_manager'
    type = SystemObjectTypes.CORE_MANAGER
    section = 'locales'

    def __init__(self):
        super().__init__()

        self.__locale = System.config.get(
            key=get_locale(),
            default='en_US',
            default_key='configs.locales.locale'
        )

        self.__locale_folder = Path(f'locales/{self.__locale}')

        self.log(f'Locale was set to {self.__locale}')

        dict_data = [read_json(i.as_posix()) for i in self.__locale_folder.rglob('*.json')]
        for item in dict_data:
            self._dictionary.update(**item)

    def get(self, key: str, default=None):
        return self._dictionary.get(key, default)

    def save(self, file: str, data: dict):
        write_json(self.__locale_folder / file, data)

    @property
    def locale(self):
        return self.__locale

    @locale.setter
    def locale(self, locale):
        self.__locale = locale
