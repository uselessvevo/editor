from pathlib import Path

from toolkit.utils.files import read_json
from toolkit.utils.files import write_json
from toolkit.utils.files import write_folder_info
from toolkit.utils.files import make_assets_manifest

from toolkit.managers import System
from toolkit.managers.base import BaseManager


class AssetsManager(BaseManager):

    _dictionary = {}
    _system_section = 'assets'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._theme = None
        self._theme_folder = None

        self._theme = System.config.get('ui.theme', default_key='ui.default_theme')
        self._theme_folder = Path(System.root, 'assets', 'themes', self._theme)

        assets_file = self._theme_folder.joinpath('assets.json')
        current_size, taken_size = write_folder_info(self._theme_folder)

        if not assets_file.exists() or current_size > taken_size:
            data = make_assets_manifest(
                prefix='shared',
                root=System.root,
                folder=self._theme_folder,
                file_formats=System.config.get('managers.assets.file_formats'),
                path_slice=-2,
            )
            write_json(assets_file, data)
            self._dictionary.update(**data)
        else:
            self._dictionary.update(**read_json(assets_file))

    def get(self, key, default=''):
        return self._dictionary.get(key, default)
