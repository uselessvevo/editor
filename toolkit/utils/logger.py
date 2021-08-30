from datetime import datetime
import enum

from toolkit.utils.objects import is_debug


class MessageTypes(enum.Enum):
    INFO = 'Info'
    WARNING = 'Warning'
    CRITICAL = 'Critical'


class AbstractLogger:

    def log(self):
        raise NotImplementedError('call method must be implemented')


class DummyLogger(AbstractLogger):

    def __init__(self, **kwargs):
        self._stdout = kwargs.get('stdout', print)

    def log(self, **kwargs):
        message = kwargs.get('message', None)
        message_type = kwargs.get('message_type', MessageTypes.INFO.value).value
        debug = is_debug()
        timestamp = datetime.now().strftime('%H:%M:%S %m.%d.%Y')
        string = f'[{"DEBUG |" if debug else ""}{timestamp} | {message_type}] {message}'

        self._stdout(string)