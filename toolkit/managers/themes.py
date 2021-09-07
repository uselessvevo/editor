from pathlib import Path
from typing import Union

from toolkit.managers.base import BaseManager
from toolkit.system.manager import System
from toolkit.system.objects import SystemObject
from toolkit.system.objects import SystemObjectTypes
from toolkit.utils.files import write_folder_info


class ThemeManager(BaseManager, SystemObject):
    name = 'theme_manager'
    type = SystemObjectTypes.MANAGER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._theme = System.config.get('system.ui.theme', default_key='system.ui.default_theme')
        self._theme_folder = System.root / 'assets' / 'themes' / self._theme
        if not self._theme_folder.exists():
            self.log(f'Theme folder "{self._theme_folder}" doesn\'t exists', do_raise=True)

    def prepare_assets(self):
        assets_file = self._theme_folder.joinpath('assets.json')
        is_updated = write_folder_info(self._theme_folder)

        if not assets_file.exists() or is_updated:
            raise


def write_assets_file(assets_root: Union[str, Path], assets_folder: Union[str, Path]):
    """
    Args:
        assets_root:
        assets_folder:

    Returns:

    """
