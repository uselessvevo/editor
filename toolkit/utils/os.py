#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File os.py - 28.02.2021, 0:56
import os
import locale
import urllib.request


def get_screen_info() -> tuple:
    """
    Get screen info

    Returns:
        (tuple): width, height
    """
    if os.name == 'nt':
        import ctypes

        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        import subprocess

        output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4', shell=True, stdout=subprocess.PIPE)
        output = output.communicate()[0]
        resolution = output.split()[0].split(b'x')
        return resolution[0], resolution[1]


def get_locale() -> tuple:
    if os.system == 'nt':
        import ctypes

        windll = ctypes.windll.kernel32
        return locale.windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        return locale.getdefaultlocale()


def check_connection(host: str = 'https://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


getLocale = get_locale
getScreenInfo = get_screen_info
checkConnection = check_connection
