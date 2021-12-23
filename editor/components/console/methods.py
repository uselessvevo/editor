import os
from termcolor import colored


__all__ = (
    'get_process_id',
    'rainbow',
)


def get_process_id():
    print('Process ID is:', os.getpid())


def rainbow(text: str):
    text = list(text)
    colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'magenta',)
    color_index = 0

    for index, symbol in enumerate(text):
        if color_index == len(colors):
            color_index = 0

        text[index] = colored(symbol, colors[color_index])
        color_index += 1

    print(''.join(i for i in text))
