import os
import sys


def ftime(seconds):
    """
    Convert seconds into a human-readable format.
    """

    if seconds < 1:
        ns = seconds * 1e9
        return ftime_ns(ns)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    data = dict(d=d, h=h, m=m, s=s)
    return ', '.join(f"{data[i]}{i}" for i in data if data[i])


def ftime_ns(ns):
    """
    Convert nanoseconds into a human-readable format.
    """

    if ns < 1e3:
        return f"{ns:.2f} ns"
    elif ns < 1e6:
        return f"{ns / 1e3:.2f} \u00B5s"
    elif ns < 1e9:
        return f"{ns / 1e6:.2f} ms"
    return ftime(int(ns / 1e9))


def flatten(data):
    """
    Flatten a list of any nestedness.
    """

    result = []
    for item in data:
        if isinstance(item, (tuple, list, set)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def pbar(it):
    """
    Responsive Terminal Design progress bar. Clears the bar when complete.
    """

    total = sum(1 for _ in iter(it))
    sys.stdout.write('\x1b[?25l\x1b[s')
    it = iter(it)
    for i in range(total):
        c = next(it)
        w = os.get_terminal_size().columns

        # 22 is the amount of characters around the progress bar. Manual for now.
        z = w - 22
        l = int(i / total * z)
        fill = f"\x1b[42m{' ' * l}\x1b[0m{' ' * (z - l)}"
        p = i / total

        sys.stdout.write(f"\x1b[uProgress: |{fill}| ({p:>6.1%})\x1b[0K")
        sys.stdout.write("\x1b[B\x1b[2K")
        yield c

    fill = f"\x1b[42m{' ' * z}\x1b[0m"

    sys.stdout.write(f"\x1b[uProgress: |{fill}| ({1:>6.1%})\x1b[0K\x1b[?25h\n")
