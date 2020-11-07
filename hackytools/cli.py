import os
import argparse
import sys
import platform

def hackystats(args):

    sys.stdout.write(f"\x1b[4m{platform.platform()}\x1b[0m\n\n")
    sys.stdout.write(f"\x1b[1mCPU Freqs (0-{os.cpu_count() - 1}):\x1b[0m\n")
    for i in range(os.cpu_count()):
        with open(f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq") as f:
            freq = int(f.read().strip())
        if freq >= 1000000:
            sys.stdout.write(f"  CPU {i}: {freq/1000000:.2f} GHz\n")
        else:
            sys.stdout.write(f"  CPU {i}: {freq/1000:.0f} MHz\n")

    sys.stdout.write("\x1b[1mTemperature\x1b[0m:\n")
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        t = int(f.read().strip()) / 1000
    sys.stdout.write(f"  {t:.1f} \u00b0C | {t*9/5+32:.1f} \u00b0F\n")

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=hackystats)
    args = parser.parse_args(argv)
    if os.name == 'nt':
        sys.exit("This command only works on linux.")
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
