from pathlib import Path

from toolkit.utils.files import read_json
from toolkit.utils.files import write_json
from toolkit.managers.locales.services import get_locale

from toolkit.managers.base import ManagerMixin
from toolkit.objects.system import SystemObject, SystemConfigCategories
from toolkit.objects.system import SystemObjectTypes
from toolkit.managers.system.manager import System


class LocalesManager(ManagerMixin, SystemObject):
    section = 'locales'
    name = 'locales_manager'
    type = SystemObjectTypes.CORE_MANAGER
    config_access = SystemConfigCategories

    def __init__(self):
        super().__init__()
        self.__locale = System.config.get(
            key='toolkit.locales.locale',
            default_value=get_locale(),
            default_key='toolkit.locales.locale'
        )

        self.__locale_folder = Path(f'locales/{self.__locale}')
        self.__locale_folder = System.app_root / 'locales' / self.__locale

        self.log(f'Locale was set to {self.__locale}')

        dict_data = [read_json(i.as_posix()) for i in self.__locale_folder.rglob('*.json')]
        for item in dict_data:
            self._dictionary.update(**item)

    def get(self, key: str, default: str = None):
        return self._dictionary.get(key, f'{key}@{self.locale}')

    def save(self, file: str, data: dict):
        write_json(self.__locale_folder / file, data)

    @property
    def locale(self):
        return self.__locale

    @locale.setter
    def locale(self, locale):
        self.__locale = locale
