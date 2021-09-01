import os
import glob
from anytree import Node
from anytree import RenderTree

from toolkit.managers.base import BaseManager

from toolkit.system.manager import System
from toolkit.system.objects import SystemObject
from toolkit.system.objects import SystemObjectTypes
from toolkit.utils.files import read_json_files

from toolkit.utils.files import read_json
from toolkit.utils.logger import MessageTypes
from toolkit.utils.objects import import_string


class PluginSystemObject(SystemObject, Node):
    type = SystemObjectTypes.PLUGIN


class AppConfigManager(BaseManager):
    system_section = 'apps'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._apps = {}

    def load(self, key, file: str):
        self._dictionary.update({key: read_json(file)})
        self.log(f'{key} / {file} was loaded')

    def unload(self, key: str):
        if key not in self._dictionary:
            raise KeyError(f'key "{key}" not found')

        self._dictionary.pop(key)

    @staticmethod
    def make_node(name: str, parent: str) -> PluginSystemObject:
        name = System.get_object(name)
        return PluginSystemObject(name=name, parent=parent)

    def load_plugins(self, plugins_root: str = 'plugins', manifest_file: str = 'manifest.json'):
        """
        Load all plugins from `plugins_folder` defined in `manifest_file`
        """
        manifest_data = read_json(f'{plugins_root}/{manifest_file}')

        for plugin in manifest_data.get('plugins'):
            plugin_name = plugin.get('name')
            plugin_folder = f'{plugins_root}/{plugin_name}'

            if not os.path.exists(plugin_folder):
                self.log(f'Plugin "{plugin_name}" was not found', MessageTypes.WARNING)
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


def load_plugins(plugins_folder: str = 'plugins'):
    # Read manifest.json file to get full info about plugins
    manifest_data = read_json(f'{plugins_folder}/manifest.json')
    plugins = [f"plugins.{i.get('exec')}" for i in manifest_data.get('plugins')]
    System.add_objects(*plugins)

    config_files = [glob.glob(f'{plugins_folder}/{i}/{i}/configs/*.json') for i in os.listdir(plugins_folder)]
    config_files = read_json_files(*config_files)
    System.config.update(config_files)
