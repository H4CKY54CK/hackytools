from urllib.request import urlopen
import urllib.error
import sys
import subprocess
import argparse


def fetchip(*, protocols:list=None, local:bool=False, timeout:float=3.0, args=None):
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
            protocols = []
            for i in args.protocols:
                if i in urls:
                    protocols.append(i)
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
        return '\n'.join(results.values()) if results else None
    return results or '???'


def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser(description="A simple tool that shows your local/public IP")
    
    parser.add_argument('protocols', nargs='*', type=int, default=[4],
                        help="return one or more protocols: choose from (4, 6) - (omitting this argument fetches both)")
    parser.add_argument('--timeout', '-t', dest='timeout', type=float, default=3.0,
                        help="set a timeout period for the request made - (defaults to 3 sec)")
    parser.add_argument('--local', '-l', dest='local', action='store_true',
                        help="include your local IP address in the results")
    parser.set_defaults(func=fetchip)

    args = parser.parse_args(argv)
    return args.func(args=args)
