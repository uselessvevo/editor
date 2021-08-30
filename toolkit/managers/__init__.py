#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File __init__.py - 02.03.2021, 15:33
from toolkit.system.manager import System


def tr(key, **kwargs):
    """
    This is a shortcut to LocalesManager's 'get' method
    Args:
        key (str) - translation key (Package.Module.Test)
        kwargs to format string
    Returns:
        formatted string
    Example:
        {'Package.Module.Test': 'This is a test, {name}', ...}
        >>> tr('Package.Module.Test', name='Joe')
    """
    return System.get_object('LocalesManager').get(key, **kwargs)


def get_file(key, default=''):
    """
    This is a shortcut to ResourcesManager's 'get' method with some additions
    Args:
        key (str) - file
        default (any/prefer str) - default value if file not found
        kwargs for QPixmap/QSVG
    Returns:
        file path
    Example:
        >>> get_file('AppIcon', 'DefaultValue')
    """
    # TODO: add file format support/check
    return System.get_object('AssetsManager').get(key, default)


def get_font(key, default='Arial'):
    return System.get_object('AssetsManager').get(key, default)


getFile = get_file
getFont = get_font
