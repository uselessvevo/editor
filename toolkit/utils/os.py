import os
import sys
import locale
import subprocess
import urllib.error
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


def get_locale() -> str:
    if os.system == 'nt':
        import ctypes

        windll = ctypes.windll.kernel32
        return locale.windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        return locale.getdefaultlocale()[0]


def check_connection(host: str = 'https://google.com'):
    try:
        urllib.request.urlopen(host, timeout=3)
        return True
    except urllib.error.URLError:
        return False


def call_subprocess(args, exit_or_raise: bool = False):
    cp = subprocess.run(args)
    try:
        cp.check_returncode()
    except subprocess.CalledProcessError:
        if exit_or_raise:
            sys.exit(cp.returncode)
        raise subprocess.CalledProcessError


getLocale = get_locale
getScreenInfo = get_screen_info
checkConnection = check_connection
