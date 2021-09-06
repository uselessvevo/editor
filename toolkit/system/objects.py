import enum
from toolkit.utils.logger import DummyLogger
from toolkit.utils.logger import MessageTypes


class SystemObjectTypes(enum.Enum):
    # System
    SYSTEM_CORE = 'system_core'
    SYSTEM_MANAGER = 'system_manager'

    # Objects
    OBJECT = 'object'
    UTILITY = 'utility'

    # Applications and plugins
    PLUGIN = 'plugin'
    MANAGER = 'manager'

    # Etc.
    UNSPECIFIED = 'unspecified'


class SystemObject:
    name = None
    type = None
    logger = DummyLogger

    def __init__(self, **kwargs) -> None:
        self.logger = kwargs.get('logger', self.logger)()

        if not self.name:
            self.name = self.__class__.__name__

        if not self.type:
            self.log(f'Object "{self.name}" has no type specified', MessageTypes.WARNING)
            self.type = SystemObjectTypes.UNSPECIFIED

    def log(self, message: str, message_type: MessageTypes = MessageTypes.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <name: {self.name} type: {self.type.value}>'
