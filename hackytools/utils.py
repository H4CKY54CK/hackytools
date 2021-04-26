from collections import namedtuple
import math



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


def ftime(seconds, kind=None):
    if kind == 'macro':
        return ftime_seconds(seconds)
    return ftime_ns(seconds * 1000000000)


def ftime_seconds(seconds, unit=None):
    """
    Convert seconds into a human-readable format (up to weeks).
    """

    if unit in ('ns', 'nanoseconds'):
        seconds /= 1000000000
    elif unit in ('us', 'microseconds'):
        seconds /= 1000000
    elif unit in ('ms', 'milliseconds'):
        seconds /= 1000
    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    year, week = divmod(week, 52)
    data = dict(year=year, week=week, day=day, hour=hour, minute=minute, second=second)
    return ', '.join(f"{int(data[i])}{i[0]}" for i in data if data[i])


def ftime_ns(nanoseconds):
    """
    Convert nanoseconds into a human-readable format (down to nanoseconds).
    """

    if nanoseconds < 1000:
        return "%.2f ns" % (nanoseconds)
    elif nanoseconds < 1000000:
        return "%.2f \u00B5s" % (nanoseconds / 1000)
    elif nanoseconds < 1000000000:
        return "%.2f ms" % (nanoseconds / 1000000)
    return "%.2f s" % (nanoseconds / 1000000000)


def smiter(iterable):
    """
    Returns a namedtuple that is aware of its first and last items by wrapping each
    item in a namedtuple with several useful attributes. Keep in mind, an iterable
    containing a single item will result in it being both first and last.

    Attributes
    ----------
    value - an object from the given iterable
    first - whether it's the first element
    last - whether it's the last element
    """

    _smart = namedtuple("SmartIter", ('value', 'first', 'last'))
    it = iter(iterable)
    first, last = True, False
    peek = next(it, None)
    while peek is not None:
        item, peek = peek, next(it, None)
        if peek is None:
            last = True
        yield _smart(item, first, last)
        first = False


def splitint(item):
    """
    Split an integer into decimal places (ones, tens, hundreds, etc) using math.
    """

    if isinstance(item, int):
        return [item // (10 ** i) % 10 for i in range(math.floor(math.log10(item)), -1, -1)]
    return tuple(item)
