import argparse
import sys
from .bork import bork
from .utils import whatsmyip
from .spriteit import spriteit
from .gifit import gifit
from .network_monitor import testwork
import os


def main(argv=None):
    argv = (argv or sys.argv)
    # Grab script name and location.
    argv[0] = os.path.splitext(os.path.basename(argv[0]))[0]

    # Create ArgumentParser
    parser = argparse.ArgumentParser(prog=argv[0])
    subparsers = parser.add_subparsers()

    # Init the different SubParsers for the Command Line Tool.
    bork_parser = subparsers.add_parser('bork')
    bork_parser.set_defaults(func=bork)

    whatsmyip_parser = subparsers.add_parser('whatsmyip')
    whatsmyip_parser.add_argument('--local', '-l', action='store_true', help='get local IP instead of public IP')
    whatsmyip_parser.set_defaults(func=whatsmyip)

    spriteit_parser = subparsers.add_parser('spriteit')
    spriteit_parser.add_argument('source')
    spriteit_parser.add_argument('output', nargs='?', default='sprites')
    spriteit_parser.add_argument('-x', '--width', dest='width', type=int, default=None)
    spriteit_parser.add_argument('-y', '--height', dest='height', type=int, default=None)
    spriteit_parser.add_argument('-xy', '--size', dest='size', type=int, default=None)
    spriteit_parser.set_defaults(func=spriteit)

    gifit_parser = subparsers.add_parser('gifit')
    gifit_parser.add_argument('source', type=str, help='source directory to make the gif with')
    gifit_parser.add_argument('output', type=str, help='the desired final output filename')
    gifit_parser.set_defaults(func=gifit)

    testwork_parser = subparsers.add_parser('whatsmyspeed')
    testwork_parser.add_argument('--quiet', '-q', dest='quiet', action='store_true', help="don't show any output")
    testwork_parser.add_argument('--repeat', '-r', dest='repeat', default=3, type=int, help='best of N')
    testwork_parser.add_argument('--last', default=0, type=int, help="output the last N results")
    testwork_parser.add_argument('--debug', action='store_true')
    testwork_parser.set_defaults(func=testwork)

    args = parser.parse_args(argv)
    return args.func(args)
