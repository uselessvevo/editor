import os
import glob
from toolkit.managers.base import BaseManager

from toolkit.objects.system import SystemObject
from toolkit.objects.system import SystemObjectTypes
from toolkit.utils.files import read_json_files

from toolkit.utils.files import read_json
from toolkit.logger import Messages
from toolkit.utils.objects import import_string


class PluginSystemObject(SystemObject):
    type = SystemObjectTypes.PLUGIN


class AppConfigManager(BaseManager):
    name = 'app_config_manager'
    type = SystemObjectTypes.CORE_MANAGER
    section = 'apps'

    def __init__(self):
        self._apps = {}
        super().__init__()

    def load(self, key, file: str):
        self._dictionary.update({key: read_json(file)})
        self.log(f'{key} / {file} was loaded')

    def unload(self, key: str):
        if key not in self._dictionary:
            raise KeyError(f'key "{key}" not found')

        self._dictionary.pop(key)

    def load_plugins(self, plugins_root: str = 'plugins', manifest_file: str = 'manifest.json'):
        """
        Load all plugins from `plugins_folder` defined in `manifest_file`
        """
        manifest_data = read_json(f'{plugins_root}/{manifest_file}')

        for plugin in manifest_data.get('plugins'):
            plugin_name = plugin.get('name')
            plugin_folder = f'{plugins_root}/{plugin_name}'

            if not os.path.exists(plugin_folder):
                self.log(f'Plugin "{plugin_name}" was not found', Messages.WARNING)
                continue

            if not os.path.exists(f'{plugin_folder}/configs/plugin.json'):
                self.log(f'Can\'t find `plugin.json` file')
                continue

            if not plugin.get('setup'):
                import_string(f"{'.'.join(plugin.get('exec').split('.')[:-2])}.setup.setup")

            plugin_config_files = [glob.glob(f'{plugins_root}/{plugin_name}/configs/*.json')
                                   for _ in os.listdir(plugins_root)]

            self._dictionary.update(**read_json_files(plugin_config_files))

            plugin_config = self._dictionary.get('')

            # TODO: make a way to collect dependencies of all plugins and then create `PluginSystemObject` nodes
            # System.add_object(plugin.get('exec'))
            # System.config.update(read_configs(*plugin_config_files))
