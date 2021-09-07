from pathlib import Path

from toolkit.system.objects import SystemObject
from toolkit.utils.files import read_json
from toolkit.utils.files import write_json
from toolkit.utils.files import write_assets_file
from toolkit.utils.files import write_folder_info

from toolkit.system.manager import System
from toolkit.managers.base import BaseManager


class AssetsManager(BaseManager, SystemObject):
    name = 'assets_manager'
    system_section = 'assets'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._theme = None
        self._theme_folder = None

        self._theme = System.config.get('configs.ui.theme', default_key='configs.ui.default_theme')
        self._theme_folder = Path('assets', 'themes', self._theme)

        assets_file = self._theme_folder.joinpath('assets.json')
        is_updated = write_folder_info(self._theme_folder)

        if not assets_file.exists() or is_updated:
            data = write_assets_file(
                prefix='shared',
                root=System.root,
                folder=self._theme_folder,
                file_formats=System.config.get('configs.managers.assets.file_formats'),
                path_slice=-2
            )
            write_json(assets_file, data)
            self._dictionary.update(**data)
        else:
            self._dictionary.update(**read_json(assets_file))

    def get(self, key: str, default: str = ''):
        return self._dictionary.get(key, default)

    @property
    def theme(self):
        return self._theme

    @property
    def theme_folder(self):
        return self._theme_folder
