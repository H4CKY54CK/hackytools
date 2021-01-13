import sys
import argparse
from speedtest import Speedtest
import time
import sqlite3
import os



def testwork(args):

    # database = os.path.abspath(os.path.join(os.path.dirname(__file__), 'networkdata.db'))
    database = os.path.join(os.path.expanduser('~'), 'networkdata.db')
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    if args.last:
        cursor.execute("SELECT * FROM network")
        results = list(reversed(cursor.fetchall()[-args.last:]))
        for x,y,z in results:
            print(f"{time.strftime('%c', time.localtime(x))}: Down: {y / 1000000:.1f} Mbps | Up: {z / 1000000:.1f} Mbps")
        return

    if not args.quiet or args.debug:
        print(f"Please wait while the network is being tested ({args.repeat} times)")

    speed = Speedtest()
    speed.get_best_server()
    down = round(max([speed.download() for i in range(args.repeat)]))
    up = round(max([speed.upload() for i in range(args.repeat)]))

    if not args.quiet or args.debug:
        print(f"Download: {down / 1000000:.1f} Mbps")
        print(f"Upload: {up / 1000000:.1f} Mbps")

    if args.debug:
        return

    if not args.quiet:
        print(f"Saving data to database {database}...")

    now = round(time.time())
    cursor.execute("CREATE TABLE IF NOT EXISTS network (utc INTEGER PRIMARY KEY, download INTEGER, upload INTEGER)")
    cursor.execute("INSERT INTO network VALUES (?, ?, ?)", (now, down, up))
    connection.commit()

    if not args.quiet:
        print("Done.")
