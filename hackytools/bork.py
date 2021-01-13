import os
import sys
import shutil
import platform
import argparse
import subprocess
import re


def details():
    sys.stdout.write(f"\x1b[4m{platform.platform()}\x1b[0m\n\n")


def frequency():
    path = f"/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
    if os.path.exists(path):
        sys.stdout.write(f"\x1b[4mCPU Freqs (0-{os.cpu_count() - 1})\x1b[0m\n")
    for i in range(os.cpu_count()):
        path = f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq"
        if os.path.exists(path):
            with open(path) as f:
                data = int(f.read()) / 1000000
            sys.stdout.write(f"  CPU {i}: {data:.2f} GHz\n")


def temperature():
    path = "/sys/class/thermal/thermal_zone0/temp"
    if os.path.exists(path):
        with open(path) as f:
            data = int(f.read()) / 1000
        sys.stdout.write(f"\x1b[4mTemperature\x1b[0m\n  {data:.1f}\u00b0C | {data * 9 / 5 + 32:.1f}\u00b0F\n")

    # Specific to my device only.
    # else:
    #     process = subprocess.run('sensors nvme-pci-0100 amdgpu-pci-0400', capture_output=True, shell=True)
    #     return_code = process.returncode

    #     if process.returncode != 0:
    #         return

    #     output = process.stdout.decode()

    #     cpu_pattern = re.compile(r'(Composite: *\+)(\d+(\.\d*))')
    #     gpu_pattern = re.compile(r'(edge: *\+)(\d+(\.\d*))')

    #     ctc = float(cpu_pattern.search(output).group(2))
    #     gtc = float(gpu_pattern.search(output).group(2))
    #     ctf = ctc * 9 / 5 + 32
    #     gtf = gtc * 9 / 5 + 32

    #     cpu_temp = f"{ctc:.1f}\u00b0C | {ctf:.1f}\u00b0F"
    #     gpu_temp = f"{gtc:.1f}\u00b0C | {gtf:.1f}\u00b0F"

    #     sys.stdout.write(f"\x1b[4mCPU Temp\x1b[0m\n  {cpu_temp}\n\x1b[4mGPU Temp\x1b[0m\n  {gpu_temp}\n")


def bork(args):
    details()
    frequency()
    temperature()
