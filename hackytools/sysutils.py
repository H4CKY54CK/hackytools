import os
import sys
import platform
import subprocess
import argparse

# Create our own exception. Common practise for exceptions
class InfoError(Exception):
    pass


def details():
    sys.stdout.write(f"\x1b[4m{platform.platform()}\x1b[0m\n\n")


def frequency():
    uname = platform.uname()
    if uname.system == 'Linux':
        path = f"/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
        if os.path.exists(path):
            sys.stdout.write(f"\x1b[4mCPU Freqs (0-{os.cpu_count() - 1})\x1b[0m\n")
        for i in range(os.cpu_count()):
            path = f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq"
            if os.path.exists(path):
                with open(path) as f:
                    data = int(f.read()) / 1000000
                sys.stdout.write(f"  CPU {i}: {data:.2f} GHz\n")
    elif uname.system == 'Windows':
        # sys.stdout.write('=' * 10 + ' System Information ' + '=' * 10 + '\nSystem:' + ' ' * (len(uname.system) // 2)
        #                 + '\t Hostname:' + ' ' * (len(uname.node) // 2)
        #                 + '\t Release:' + ' ' * (len(uname.release) // 2)
        #                 + '\t Version:' + ' ' * (len(uname.version) // 2)
        #                 + '\t Machine:' + ' ' * (len(uname.machine) // 2)
        #                 + '\t Processor:\t\n'
        #                 + f'{uname.system}\t' + ' ' * (len(uname.system) // 2)
        #                 + f'{uname.node}\t' + ' ' * (len(uname.node) // 2)
        #                 + f'{uname.release}\t' + ' ' * (len(uname.release) // 2)
        #                 + f'{uname.version}\t' + ' ' * (len(uname.version) // 2)
        #                 + f'{uname.machine}\t' + ' ' * (len(uname.machine) // 2)
        #                 + f'{uname.processor}') TODO Implement this later as a different command
        try:
            data = str(subprocess.run(
                ['powershell', '-Command', 'Get-WmiObject -Class Win32_Processor -Property CurrentClockSpeed'],
                capture_output=True))
            max_freq = int(data[data.find(': \\r\\nCurrentClockSpeed : '):].split('\\r')[1].split(':')[1][1:])

            data = subprocess.check_output("wmic cpu get CurrentClockSpeed", shell=True)
            data = data.decode('utf-8')
            current_freq = int(data[data.find('\r\r'):].split(' ')[0].split('\n')[1])
            # place holder print statement
            sys.stdout.write(f"\x1b[4mCPU ID\t Current Freq\t Max Freq\x1b[0m\n")
            for cpu in range(os.cpu_count()):
                sys.stdout.write(f"CPU{cpu}\t {current_freq}\t " + " " * (len("Current Freq") // 2) + f" {max_freq}\n")
        except Exception as e:
            raise InfoError(f"Could Not Determine CPU frequency: {e}")
        else:
            pass  # TODO Finish off getting other Information from Windows


def temperature():
    path = "/sys/class/thermal/thermal_zone0/temp"
    if os.path.exists(path):
        with open(path) as f:
            data = int(f.read()) / 1000
        sys.stdout.write(f"\x1b[4mTemperature\x1b[0m\n  {data:.1f}\u00b0C | {data * 9 / 5 + 32:.1f}\u00b0F\n")

# TODO: Consider having these build a response, and then return it
def sysutils(args):
    result = [
        details(),
        frequency(),
        temperature(),
    ]
    return '\n'.join(i for i in result if i)

def main(argv=None):

    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser(description="A simple tool that shows some basic system stats at a glance.")
    parser.set_defaults(func=sysutils)

    args = parser.parse_args(argv)
    return args.func(args=args)
