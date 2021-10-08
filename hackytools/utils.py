from collections import namedtuple
import math
import itertools
import re



def combutations(data, n=None, *, reverse=False):
    """
    Return a combination of all unique permutations of the provided data.
    """

    if not reverse:
        yield from (item for i in range(1, (n or len(data)) + 1, 1) for item in itertools.combinations(data, i))
    else:
        yield from (item for i in range(n or len(data), 0, -1) for item in itertools.combinations(data, i))


def flatten(data):
    """
    Flatten a list/tuple/set of any nestedness.
    """

    result = []
    for item in data:
        if isinstance(item, (tuple, list, set)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def ftime_ns(nanoseconds, precision=2, spaced=None):
    """
    Convert nanoseconds into a human-readable format (small units).
    """

    # shorten the variable name to keep line length under 100 lol
    ns = nanoseconds
    if ns < 1000:
        if spaced is True or spaced is None:
            return "{ns:.{precision}f} ns".format(ns=ns, precision=precision)
        return "{ns:.{precision}f}ns".format(ns=ns, precision=precision)

    elif ns < 1000000:
        if spaced is True or spaced is None:
            return "{ns:.{precision}f} \u00b5s".format(ns=ns / 1000, precision=precision)
        return "{ns:.{precision}f}\u00b5s".format(ns=ns / 1000, precision=precision)

    elif ns < 1000000000:
        if spaced is True or spaced is None:
            return "{ns:.{precision}f} ms".format(ns=ns / 1000000, precision=precision)
        return "{ns:.{precision}f}ms".format(ns=ns / 1000000, precision=precision)

    if spaced is True or spaced is None:
        return "{ns:.{precision}f} s".format(ns=ns / 1000000000, precision=precision)
    return "{ns:.{precision}f}s".format(ns=ns / 1000000000, precision=precision)


def ftime(seconds, spaced=None):
    """
    Convert seconds into a human-readable format (small units).
    """

    return ftime_ns(seconds * 1000000000, spaced=spaced)


def rem_time(seconds, abbreviate=False, spaced=None):
    """
    Convert seconds into remaining time (up to years).
    """

    units = ['years', 'weeks', 'days', 'hours', 'minutes', 'seconds']
    data = {item: 0 for item in units}

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    years, weeks = divmod(weeks, 52)

    data.update(seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks, years=years)

    if abbreviate is True:
        if spaced is True:
            return ', '.join('%d %s' % (v, k[0]) for k,v in data.items() if v != 0)
        return ', '.join('%d%s' % (v, k[0]) for k,v in data.items() if v != 0)

    result = []
    for k,v in data.items():
        if v > 1:
            if spaced is True or spaced is None:
                result.append('%d %s' % (v, k))
            elif spaced is False:
                result.append('%d%s' % (v, k))
        elif v == 1:
            if spaced is True or spaced is None:
                result.append('%d %s' % (v, k[:-1]))
            elif spaced is False:
                result.append('%d%s' % (v, k[:-1]))

    return ', '.join(result)


def splitint(item):
    """
    Split an integer into decimal places (ones, tens, hundreds, etc) using math, if possible.
    """

    if item == 0:
        return [0]
    elif isinstance(item, int):
        return [item // (10 ** i) % 10 for i in range(math.floor(math.log10(item)), -1, -1)]
    return list(map(int,item))
