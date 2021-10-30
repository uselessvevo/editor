import os
import sys
import subprocess


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


def call_subprocess(args, exit_or_raise: bool = False) -> None:
    cp = subprocess.run(args)
    try:
        cp.check_returncode()
    except subprocess.CalledProcessError:
        if exit_or_raise:
            sys.exit(cp.returncode)
        raise subprocess.CalledProcessError


getScreenInfo = get_screen_info
