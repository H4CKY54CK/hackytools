from .netutils import fetchip
from .sysutils import sysutils
import os
import sys
import argparse


def main(argv=None):
    """
    The top-level parser that delegates entry points to subcommands, so that
    they behave like normal, top-level commands.
    """

    argv = (argv or sys.argv)
    argv[0] = os.path.splitext(os.path.basename(argv[0]))[0]
    parser = argparse.ArgumentParser(prog=argv[0])
    subparsers = parser.add_subparsers()

    netutils_parser = subparsers.add_parser(name=argv[0],
                                            description="A simple tool that shows your local/public IP")
    netutils_parser.add_argument('protocols', nargs='*', type=int,
                        help="return one or more protocols: choose from (4, 6) - (omitting this argument fetches both)")
    netutils_parser.add_argument('--timeout', '-t', dest='timeout', type=float, default=3.0,
                        help="set a timeout period for the request made - (defaults to 3 sec)")
    netutils_parser.add_argument('--local', '-l', dest='local', action='store_true',
                        help="include your local IP address in the results")
    netutils_parser.set_defaults(func=fetchip)


    sysutils_parser = subparsers.add_parser(name=argv[0],
                                            description="A simple tool that shows some basic system stats at a glance.")
    sysutils_parser.set_defaults(func=sysutils)


    args = parser.parse_args(argv)
    return args.func(args=args)
