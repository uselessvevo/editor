"""
CloudyEditor Console utils
"""
import os
import re


def discover_methods(path, **kwargs):
    if not os.path.exists(path):
        raise OSError(f'Path "{path}" not found')

    pattern = kwargs.get('pattern', '*')
