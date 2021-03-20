from collections import namedtuple


def ftime(seconds):
    """
    Convert seconds into a human-readable format (up to weeks).
    """

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    w, d = divmod(d, 7)
    y, w = divmod(w, 52)
    data = dict(y=y, w=w, d=d, h=h, m=m, s=s)
    return ', '.join(f"{data[i]}{i}" for i in data if data[i])


def ftime_ns(ns):
    """
    Convert nanoseconds into a human-readable format (down to nanoseconds).
    """

    if ns < 1000:
        return f"{ns:.2f} ns"
    elif ns < 1000000:
        return f"{ns / 1000:.2f} \u00B5s"
    elif ns < 1000000000:
        return f"{ns / 1000000:.2f} ms"
    return f"{ns / 1000000000:.2f} s"


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


_smart = namedtuple("SmartIter", ('value', 'first', 'last'))


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

    it = iter(iterable)
    first, last = True, False
    peek = next(it, None)
    while peek is not None:
        item, peek = peek, next(it, None)
        if peek is None:
            last = True
        yield _smart(item, first, last)
        first = False