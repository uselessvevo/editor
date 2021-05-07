#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File system.py - 07.03.2021, 16:40
import json
import os
from typing import List
from dotty_dict import Dotty

from toolkit.utils.files import read_json
from toolkit.utils.files import update_json
from toolkit.utils.files import write_json
from toolkit.utils.objects import import_string


class SystemConfig(Dotty):

    def __init__(self, defaults: dict = None):
        dictionary = {}
        if defaults:
            dictionary.update(**defaults)

        super().__init__(dictionary=dictionary)

    def get(self, key, default=None, default_key=None):
        if default_key:
            default = super().get(default_key, default)
        return super().get(key) or default

    def set(self, key, value):
        self[key] = value

    def save(self, key):
        """
        Args:
            key (str): f.e. 'dictionary.nested.key'

        Returns:
            None
        """
        update_json(key, self[key])

    def from_json_file(self, file, **kwargs):
        self._dictionary.update(**read_json(file, **kwargs))

    def __repr__(self):
        return f'({self.__class__.__name__}) <items: {list(self._data.keys())[:2]}>'


class SystemManager:
    """
    System is the core manager
    Provides easy access to instances, settings and etc.
    """

    version = '0.0.1'
    config_class = SystemConfig

    def __init__(self):
        self._root = None
        self._objects = {}
        files = self.custom_read_json_files([f'config/{i}' for i in os.listdir('config')])
        self._config = self.config_class(defaults=files)
        print(f'* * * * Starting system {self.version}')

    def custom_read_json_files(self, files, skip_error=True, create=False):
        """
        Args:
            files (List[str]): list of files
            skip_error (bool): set True if you need to skip error
        """
        # Clear duplicates
        files = set(files)
        collect = {}

        for file in files:
            # Get file without path and extension
            key = os.path.basename(file)
            key = os.path.splitext(key)[0]

            if create and not os.path.exists(file):
                write_json(file, {})

            try:
                with open(file, encoding='utf-8') as output:
                    collect[key] = json.load(output)

            except (OSError, FileNotFoundError, json.decoder.JSONDecodeError) as err:
                if skip_error:
                    collect[key] = {}
                else:
                    raise err

            if isinstance(collect[key], dict):
                collect[key].update({'__file__': file})

        return collect

    def set_system_root(self, root):
        """
        Args:
            root (str): project root path

        Returns:
            None
        """
        if not os.path.exists(root):
            raise FileNotFoundError('File or path not found')

        if os.path.isfile(root):
            print(f'* * * * Root set to {root}')
            self._root = os.path.split(root)[0]

    def init(self):
        for key, instance in self._objects.items():
            print(f'* * * * Init object {instance}')
            self._objects[key] = instance()

    def add_objects(self, *objects: str):
        objects = [i for i in objects if i in objects]

        for obj_str in objects:
            print(f'* * * * Adding object {obj_str}')
            self.add_object(*import_string(obj_str))

    def add_object(self, instance: type, name: str) -> None:
        """
        Args:
            instance (type): object that will be added
            name (str): object key name
        """
        if name in self._objects:
            raise KeyError(f'Object {name} already added')

        self._objects[name] = instance
        print(f'* * * * Object {name}/{instance} added')

    def remove_object(self, name: str) -> None:
        if name not in self._objects:
            raise KeyError(f'Object {name} not found')

        del self._objects[name]
        print(f'* * * * Object {name} has been removed')

    def get_object(self, name: str) -> type:
        """
        Get object by name

        Args:
            name (str): object name

        Returns:
            object
        """
        if name not in self._objects:
            raise KeyError(f'Object {name} not found')

        return self._objects[name]

    def get_objects_list(self) -> List[object]:
        return list(self._objects.keys())

    @property
    def root(self):
        return self._root

    @property
    def config(self):
        return self._config

    @property
    def objects(self):
        return self._objects

    def __str__(self):
        return f'<{self.get_objects_list()}>'

    def __repr__(self):
        return f'({self.__class__.__name__}) <objects: {self.get_objects_list()[:5]}>'


System = SystemManager()
