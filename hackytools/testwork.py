import sys
import argparse
from speedtest import Speedtest
import time
import sqlite3
import os



def testwork(args):

    database = os.path.join(os.path.expanduser('~'), 'networkdatarecords.db')
    bits = 1000000
    
    if args.debug:
        print(args)
        return

    if args.clear:
        if os.path.exists(database):
            os.unlink(database)
            return "Cleared database."
        return "Database already cleared."

    if args.last:
        if not os.path.exists(database):
            return "You must run at least 1 test so that there is something in the database to report on."
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM network")
        results = cursor.fetchall()[-args.last:]
        print(f"Here are your last {args.number} results (from oldest to newest)")
        for w,x,y,z in results:
            print(f" - {time.strftime('%x %X', time.localtime(w))}: Down: {x / bits:.2f} Mbps | Up: {y / bits:.2f} Mbps | Ping: {z:.2f} ms")
        return

    if not args.quiet:
        print(f"Please wait while the network is being tested ({args.number} times)")

    speed = Speedtest()
    speed.get_best_server()

    # Print separately, so the user doesn't get bored while they're waiting.
    download = []
    for i in range(args.number):
        download.append(speed.download())
        if args.number > 1:
            print(f"\r{i + 1} of {args.number} download tests done...", end='')
    down = max(download)
    if not args.quiet:
        print(f"  Download: {down / bits:.2f} Mbps")

    # Print separately, so the user doesn't get bored while they're waiting.
    upload = []
    for i in range(args.number):
        upload.append(speed.upload())
        if args.number > 1:
            print(f"\r{i + 1} of {args.number} download tests done...", end='')
    up = max(upload)
    if not args.quiet:
        print(f"  Upload: {up / bits:.2f} Mbps")

    ping = speed.results.ping
    if not args.quiet:
        print(f"  Ping: {ping:.2f} ms")
        print(f"Saving data to database {database}...")

    now = round(time.time())
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS network (utc INTEGER PRIMARY KEY, download INTEGER, upload INTEGER, ping INTEGER)")
    cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?)", (now, down, up, ping))
    connection.commit()


def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--number', '-n', dest='number', default=1, type=int, help='best of N')
    parser.add_argument('--last', '-l', dest='last', nargs='?', default=None, const=5, type=int, help="output the last N results")
    parser.add_argument('--quiet', '-q', dest='quiet', action='store_true', help="don't show any output")
    parser.add_argument('--clear', action='store_true', help="clear entire database of records")
    parser.add_argument('--debug', action='store_true', help='debug mode')
    parser.set_defaults(func=testwork)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return "Cancelled by user. Shutting down after this test finishes."


if __name__ == '__main__':
    sys.exit(main())