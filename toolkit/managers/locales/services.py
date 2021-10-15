import os
import locale


def get_locale() -> str:
    if os.system == 'nt':
        import ctypes

        windll = ctypes.windll.kernel32
        return locale.windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        return locale.getdefaultlocale()[0]
