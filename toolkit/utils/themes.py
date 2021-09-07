#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File themes.py - 01.02.2021, 14:31
import os
import re
import importlib
import importlib.util

from toolkit.managers import get_file
from toolkit.utils.files import read_json


def parse_stylesheet(path, keys=None):
    """
    Args:
        path (str or os.PathLike) - path to theme file
        keys (dict) - additional value
    """
    if not os.path.exists(f'{path}/theme.qss'):
        with open(f'{path}/theme.template.qss', encoding='utf-8') as output:
            # Template pattern and variables
            pattern = r'((\@)([A-Za-z]+[\d]+[\w@]*|[A-Za-z]+[\w@]*))'
            variables = read_json(f'{path}/variables.json')
            variables.update(keys)

            # Template content
            stylesheet = output.read()
            matches = re.findall(pattern, stylesheet)

            for match in matches:
                stylesheet = stylesheet.replace(match[0], variables[match[0]])

        with open(f'{path}/theme.qss', 'w') as output:
            output.write(stylesheet)
    else:
        # Create empty theme file
        with open(f'{path}/theme.qss', encoding='utf-8') as output:
            stylesheet = output.read()

    return stylesheet


def get_theme(theme):
    """
    Parse and get stylesheet

    Args:
        theme (str): theme name

    Returns:
        stylesheet (str): stylesheet string
    """
    theme_name = f'assets/themes/{theme}'
    themes_list = os.listdir('assets/themes')
    stylesheet = ''

    # Check if folder exists
    if not os.path.exists(theme_name):
        # Get one of theme
        if themes_list and os.path.exists(themes_list[0]):
            theme_name = f'assets/themes/{themes_list[0]}'
        else:
            theme_name = None

    if theme_name and os.path.exists(theme_name):
        stylesheet = parse_stylesheet(theme_name, {
            '@themeFolder': theme_name
        })

    return stylesheet


def get_palette(theme):
    """
    Get palette module from theme folder

    Args:
        theme (str): theme name

    Returns:
        palette (module): app.setPalette(palette.getPalette())
    """
    theme_name = f'assets/themes/{theme}'
    palette = None

    if os.path.exists(f'{theme_name}/palette.py'):
        spec = importlib.util.spec_from_file_location(
            name='palette',
            location=f'{theme_name}/palette.py'
        )
        palette = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(palette)

    return palette.getPalette()


PATTERNS = [
    r'((\@)\((.*?);(.*?)\))|'  # Method link pattern
    r'((\$)\((.*?)\))'  # Resource pattern
]


PREFIXES = {
    '$': '_resources_parser',
    '@': '_methods_parser'
}


def text_parser(text):

    def resources(args):
        filename = get_file(*args)
        view = f'<img src=\"{filename}\" alt="{filename}">'
        return view

    def methods(*args):
        return f'<a href={args[0][1]}>{args[0][0]}</a>'

    matches = re.findall(PATTERNS, text)
    matches = list(tuple(filter(None, x)) for x in matches)

    for match in matches:
        original, prefix, *arguments = match
        # result = globals()[prefixes[prefix]](*arguments)
        if prefix == '$':
            result = resources(arguments)

        elif prefix == '@':
            result = methods(arguments)

        text = text.replace(original, result)

    return text


# Qt aliases
getTheme = get_theme
getPalette = get_palette
parseStylesheet = parse_stylesheet
textParser = text_parser
