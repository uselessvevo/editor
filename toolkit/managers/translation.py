from pathlib import Path

from toolkit.system.objects import SystemObject, SystemObjectTypes
from toolkit.utils.files import read_json
from toolkit.utils.files import write_json

from toolkit.system.manager import System
from toolkit.managers.base import BaseManager
from toolkit.utils.os import get_locale


class TranslationManager(BaseManager, SystemObject):
    name = 'translation_manager'
    type = SystemObjectTypes.MANAGER
    system_section = 'translations'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)


def json_to_mo(file):
    data = read_json(file)
    template = '''msgid ""
    msgstr ""
    "MIME-Version: 1.0"
    "Content-Type: text/plain; charset=UTF-8"
    "Content-Transfer-Encoding: 8bit"
    "X-Generator: pogen-script"
    "Project-Id-Version: CloudyFF"
    "Language: {locale}"
    '''
    template = template.format({

    })

    for k, v in data.items():
        template += f'msgid "{k}"\rmsgstr "{v}"\n\n'

    with open('cloudyff/locales/en_US/Shared.po', 'w') as file:
        file.write(template)
