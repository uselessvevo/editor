from toolkit.helpers.files import read_json
from toolkit.helpers.files import write_json
from toolkit.helpers.files import write_assets_file
from toolkit.helpers.files import write_folder_info

from toolkit.managers.system.manager import System
from toolkit.managers.base import BaseManager
from toolkit.objects.system import SystemObjectTypes


class AssetsManager(BaseManager):
    name = 'assets_manager'
    section = 'managers.assets'
    type = SystemObjectTypes.CORE_MANAGER

    def __init__(self):
        super().__init__()

        self._theme = None
        self._theme_folder = None

    def init(self, *args, **kwargs):
        self._theme = System.config.get('app.ui.theme', default_key='app.ui.default_theme')
        self._theme_folder = System.app_root / 'assets' / 'themes' / self._theme

        assets_file = self._theme_folder.joinpath('assets.json')
        is_updated = write_folder_info(self._theme_folder)

        if not assets_file.exists() or is_updated:
            data = write_assets_file(
                prefix='shared',
                root=System.app_root,
                folder=self._theme_folder,
                file_formats=System.config.get('toolkit.managers.assets.file_formats'),
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
