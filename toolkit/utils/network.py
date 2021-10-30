import urllib.error
import urllib.request


def check_connection(host: str = 'https://google.com') -> bool:
    try:
        urllib.request.urlopen(host, timeout=3)
        return True
    except urllib.error.URLError:
        return False
