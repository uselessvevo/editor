import abc
import enum
from datetime import datetime
from types import MethodType
from typing import Union, Final

from toolkit.utils.objects import is_debug


class Messages(enum.Enum):
    INFO: Final = 'Info'
    WARNING: Final = 'Warning'
    CRITICAL: Final = 'Critical'
    ERROR: Final = 'Error'


class AbstractLogger(abc.ABC):

    @abc.abstractmethod
    def log(self) -> None:
        pass


class LoggerException(Exception):

    def __init__(self, exc_message: str) -> None:
        self._exc_message = exc_message

    def __str__(self) -> str:
        return self._exc_message


class DummyLogger(AbstractLogger):

    def __init__(self, **kwargs) -> None:
        self._stdout: MethodType = kwargs.get('stdout', print)

    def log(self, *args, **kwargs) -> None:
        debug: bool = is_debug()
        do_raise: bool = kwargs.get('do_raise', False)

        message: Union[str] = kwargs.get('message', None)
        timestamp: datetime.now = datetime.now().strftime('%H:%M:%S %m.%d.%Y')

        if do_raise:
            exc_type: Exception = kwargs.get('exc_type', Exception)
            exc_message: str = kwargs.get('exc_message', message)

            if not issubclass(exc_type, Exception):
                raise TypeError('Exception type (exc_type) is not an exception')

            message_type: Messages = kwargs.get('message_type', Messages.CRITICAL.value).value
            exc_message: str = (
                f'[{"DEBUG |" if debug else ""}{timestamp} | '
                f'{message_type + "]":<10} {exc_type}, {exc_message}'
            )

            raise LoggerException(exc_message)

        message_type: Messages = kwargs.get('message_type', Messages.INFO.value).value

        self._stdout(f'[{"DEBUG |" if debug else ""}{timestamp} | {message_type + "]":<10} {message}')
