from toolkit.managers.base import BaseManager


class ConfigurationManager(BaseManager):

    _system_section = 'configuration'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
