import os
import argparse
import sys


def hackystats(args):

    cpu_cur = lambda i: f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq"
    cpu_max = lambda i: f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_max_freq"
    temps = "/sys/class/thermal/thermal_zone0/temp"

    x = os.cpu_count()

    print(f"\x1b[4mCPU Freqs ({x}) (current/max)\x1b[0m")
    for i in range(x):
        with open(cpu_cur(i)) as f:
            freq = int(f.read().strip())
        with open(cpu_max(i)) as f:
            max_freq = int(f.read().strip())
        if freq > 1000000:
            print(f"  CPU{i}: {freq/1000000:,.2f} GHz (\x1b[1m{max_freq/1000000:,.2f} GHz\x1b[0m)")
        else:
            print(f"  CPU{i}: {freq/1000:,.1f} MHz (\x1b[1m{max_freq/1000:,.1f} MHz\x1b[0m)")

    print(f"\x1b[4mTemperature\x1b[0m")
    with open(temps) as f:
        t = int(f.read().strip())
    if args.fahrenheit:
        msg = f"  {t / 1000 * 9 / 5 + 32:.1f} \N{DEGREE SIGN}F"
    else:
        msg = f"  {t / 1000:.1f} \N{DEGREE SIGN}C"
    print(msg)

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--fahrenheit', '-f', action='store_true', help="show temperature in fahrenheit instead of celsius")
    parser.set_defaults(func=hackystats)
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
