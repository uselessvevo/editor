from pathlib import Path
from toolkit.utils.files import read_json
from toolkit.utils.files import write_json

from toolkit.system.manager import System
from toolkit.managers.base import BaseManager
from toolkit.utils.os import get_locale


class TranslationsManager(BaseManager):
    system_section = 'translations'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._locale = System.config.get(
            key=get_locale()[0],
            default='en_US',
            default_key='configs.locales.locale'
        )

        self._locale_folder = Path(f'locales/{self._locale}')

        self.log(f'Locale was set to {self._locale}')

        dict_data = [read_json(i.as_posix()) for i in self._locale_folder.rglob('*.json')]
        for item in dict_data:
            self._dictionary.update(**item)

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, key: str, default=None):
        return self._dictionary.get(key, default)

    def save(self, file: str, data: dict):
        write_json(self._locale_folder / file, data)

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, locale):
        self._locale = locale
