import enum
from anytree import Node
from toolkit.utils.logger import DummyLogger
from toolkit.utils.logger import MessageTypes


class SystemObjectTypes(enum.Enum):
    # Managers
    CORE_MANAGER = 'core_manager'
    PLUGIN_MANAGER = 'plugin_manager'

    # Objects
    OBJECT = 'object'
    UTILITY = 'utility'

    # Applications and plugins
    PLUGIN = 'plugin'

    # Etc.
    UNSPECIFIED = 'unspecified'


class SystemObject(Node):
    name: str = None
    section: str = None
    type: SystemObjectTypes = SystemObjectTypes.UNSPECIFIED
    logger = DummyLogger

    def __init__(self, parent: Node, *args, **kwargs) -> None:
        self.logger = kwargs.get('logger', self.logger)()

        if not self.name:
            self.name = self.__class__.__name__

        if not self.type:
            self.log(f'Object "{self.name}" has no type specified', MessageTypes.CRITICAL)
            self.type = SystemObjectTypes.UNSPECIFIED

        super().__init__(self.name, parent, *args, **kwargs)

    def log(self, message: str, message_type: MessageTypes = MessageTypes.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <hash: {self.__hash__()} name: {self.name} type: {self.type.value}>'
