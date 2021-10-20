from toolkit.managers.system.manager import System


def tr(key: str, **kwargs):
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


def get_file(key: str, default: str = ''):
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


def get_font(key: str, default: str = 'Arial'):
    return System.get_object('AssetsManager').get(key, default)


getFile = get_file
getFont = get_font
