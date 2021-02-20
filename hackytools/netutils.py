from urllib.request import urlopen
import urllib.error
import sys
import subprocess


def fetchip(*, protocols: list = None, local: bool = False, timeout: float = 3.0, args=None):
    """
    A convenience tool for getting any combination of your IPv4, IPv6, and local IP addresses.
    """

    urls = {
        4: 'https://api.ipify.org',
        6: 'https://api64.ipify.org',
    }
    if protocols is None:
        protocols = []
    if args:

        local = args.local
        if local:
            protocols = []
        else:
            protocols = [i for i in args.protocols if i in urls] or [4, 6]
        timeout = args.timeout

    results = {}
    for i in protocols:
        try:
            r = urlopen(urls[i], timeout=timeout)
            results[f'ipv{i}'] = r.read().decode().strip()
            r.close()
        except urllib.error.URLError:
            return sys.exc_info()
    if local:
        try:
            command = ['ip', 'route', 'get', '1.2.3.4']
            r = subprocess.check_output(command).decode().split()[6]
            results['local'] = r
        except IndexError:
            pass

    if args:
        return '\n'.join(results.values())
    return results
