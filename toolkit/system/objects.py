import enum

from toolkit.utils.logger import DummyLogger
from toolkit.utils.logger import MessageTypes


class SystemObjectTypes(enum.Enum):
    OBJECT = 'object'
    PLUGIN = 'plugin'
    MANAGER = 'manager'
    UTILITY = 'utility'
    APPLICATION = 'application'


class SystemObject:
    name = None
    type = None
    logger = DummyLogger

    def log(self, message: str, message_type: MessageTypes = MessageTypes.INFO):
        self.logger.log(message=message, message_type=message_type)

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger', self.logger)()

        if not self.name:
            self.name = self.__class__.__name__

        if not self.type:
            self.log(f'Object "{self.name}" has no type specified', MessageTypes.WARNING)
            self.type = SystemObjectTypes.APPLICATION

    def __repr__(self):
        return f'({self.name}) <type: {self.type.value}>'
