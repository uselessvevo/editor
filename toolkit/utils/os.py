#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File os.py - 28.02.2021, 0:56
import os


def get_screen_info():
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


getScreenInfo = get_screen_info
