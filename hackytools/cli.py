import os
import argparse
import sys
sprint = sys.stdout.write



def hackystats_g(args):
    data = {
        'freqs': [f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq" for i in range(os.cpu_count())],
        'temp': "/sys/class/thermal/thermal_zone0/temp",
    }

    for key in data:
        if key == 'freqs':
            sprint(f"\x1b[1mCPU Freqs ({len(data[key])} cores)\x1b[0m\n")
            for item in data[key]:
                with open(item) as f:
                    freq = int(f.read().strip())
                sprint(f"  {freq/1000:.0f} MHz (core {data[key].index(item)})\n")
        if key == 'temp':
            with open(data[key]) as f:
                t = int(f.read().strip())
            tc = t/1000
            tf = tc * 9 / 5 + 32
            sprint(f"Temperature: {tc:.1f} \u00b0C | {tf:.1f} \u00b0F\n")

def hackystats(args):
    if args.generator:
        return hackystats_g(args)

    cpu_cur = lambda i: f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq"
    cpu_max = lambda i: f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_max_freq"
    temps = "/sys/class/thermal/thermal_zone0/temp"

    x = os.cpu_count()

    result = ''

    result += f"\x1b[4mCPU Freqs ({x}) (current/max)\x1b[0m\n"
    for i in range(x):
        with open(cpu_cur(i)) as f:
            freq = int(f.read().strip())
        with open(cpu_max(i)) as f:
            max_freq = int(f.read().strip())
        if freq > 1000000:
            result += f"  CPU{i}: {max_freq/1000000:,.2f} GHz (\x1b[1m{freq/1000000:,.2f} GHz\x1b[0m)\n"
        else:
            result += f"  CPU{i}: {max_freq/1000:,.1f} MHz (\x1b[1m{freq/1000:,.1f} MHz\x1b[0m)\n"

    result += f"\x1b[4mTemperature\x1b[0m\n"
    with open(temps) as f:
        t = int(f.read().strip())
    if args.fahrenheit:
        result += f"  {t / 1000 * 9 / 5 + 32:.1f} \N{DEGREE SIGN}F\n"
    else:
        result += f"  {t / 1000:.1f} \N{DEGREE SIGN}C\n"
    return result

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--fahrenheit', '-f', action='store_true', help="show temperature in fahrenheit instead of celsius")
    parser.add_argument('--generator', '-g', action='store_true')
    parser.set_defaults(func=hackystats)
    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == '__main__':
    sys.exit(main())
