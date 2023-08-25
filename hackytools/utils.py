import os
import math
import hashlib
import random
import itertools
import numpy as np
import collections

from . import iterators



def combutations(iterable, n, *, reverse=False):
    """Gives you every combination of 'iterable' for every length up to (and including) 'n'.

    For example, list(combutations("abc")) would give you:
    [('a',), ('b',), ('c',), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('a', 'b', 'c')]

    :param iterable: Iterable to use for making combutations out of.
    :param n: The max length of combinations.
    """
    if not reverse:
        yield from (item for i in range(1, (n or len(iterable)) + 1, 1) for item in itertools.combinations(iterable, i))
    else:
        yield from (item for i in range(n or len(iterable), 0, -1) for item in itertools.combinations(iterable, i))


# Marked for removal.
# On second thought. hashlib only provides this in 3.11+. We provide this for any Python?
def file_digest(filename, *, algorithm="sha1", buffer=2**20):
    """
    A memory efficient function for computing the hexdigest of a given file. The algorithm used and the size of the
    buffer used for reading from the file can both be changed by using the corresponding keyword arguments.

    Note: Hashlib recently added a similar function to their module. The problem is that it is only available if you
    have that version of Python or higher. My library doesn't care what version you have.

    :param algorithm: The algorithm used to compute the hash. Can also be a function. (Default: "sha1")
    :param buffer: The max amount of bytes to read from the given file at once. (Default: 2**20)
    """
    if callable(algorithm):
        m = algorithm()
    else:
        m = hashlib.new(algorithm)
    with open(filename, "rb") as f:
        while True:
            block = f.read(buffer)
            if not block:
                break
            m.update(block)
    return m.hexdigest()


# def find(source):
#     """A Python equivalent for the linux command 'find'."""
#     try:
#         for item in os.scandir(source):
#             if item.is_symlink():
#                 continue
#             if item.is_dir():
#                 yield from find(item)
#             if item.is_file():
#                 yield item.path
#     except PermissionError:
#         pass


def flatten(data):
    """Flatten a list/tuple/set of any nestedness."""
    result = []
    for item in data:
        if isinstance(item, (tuple, list, set)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def frate(n_bytes: int, seconds: int | float, *, precision: int = 2, base: int = 2) -> str:
    """Calculate a given amount of bytes 'n_bytes' transferred over elapsed time 'seconds' and
    return the result in a human-readable format.

    :param n_bytes: The amount of bytes transferred.
    :param seconds: The elapsed time in seconds.
    :param precision: The desired float precision of the resulting amount.
    :param base: Which base system to use.
        base 10 (or 1000) uses 1000 bytes for KB, etc.
        base 2 (or 1024) uses 1024 bytes as KiB, etc.
        (Default: 10)"""

    if base in (10, 1000):
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        k = 1000
    elif base in (2, 1024):
        units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
        k = 1024
    else:
        raise ValueError("please choose between base 2 (aka 1024) and base 10 (aka 1000)")

    for i in range(len(units)):
        if n_bytes < (k ** (i + 1)):
            output = f"{(n_bytes / (k ** i)) / seconds:.{precision}f} {units[i]}/s"
            return output
    raise ValueError("exceeds maximum unit size")


def fsize(amount: int, *, base: int = 10, precision: int = 2) -> str:
    """Convert a file size into a human-readable format.

    :param amount:      The amount of bytes to convert.
    :param base:        Which base system to use. Valid values are: `10` or `1000` for KB, MB, GB, TB, etc. and `2` or
                        `1024` for KiB, MiB, GiB, TiB, etc. (Default: 10).
    :param precision:   The desired float precision of the resulting amount.
    """
    if base in (10, 1000):
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        k = 1000
    elif base in (2, 1024):
        units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
        k = 1024
    else:
        raise ValueError("please choose between base 2 (aka 1024) and base 10")
    for u in units:
        if amount < k:
            break
        amount /= k

    return "%s %s" % (round(amount, precision), u)


def ftime(seconds: float, *args, **kwargs) -> str:
    """Converts seconds to nanoseconds and then acts as an alias to ftime_ns."""
    return ftime_ns(seconds * 1000000000, spaced=spaced)


# Marked for a review. Possibly belongs in a `hackytools.formatting` submodule?
def ftime_ns(nanoseconds: int, *, precision: int = 2, spaced: bool = True) -> str:
    space = " " if spaced else ""
    if nanoseconds < 1000:
        return "%s%sns" % (format(nanoseconds, ".%df" % precision), space)
    if nanoseconds < 1000000:
        return "%s%s\u00b5s" % (format(nanoseconds / 1000, ".%df" % precision), space)
    if nanoseconds < 1000000000:
        return "%s%sms" % (format(nanoseconds / 1000000, ".%df" % precision), space)
    return "%s%ss" % (format(nanoseconds / 1000000000, ".%df" % precision), space)


def groups(iterable, size, *, fill=False, fill_value=None):
    """
    Takes a sequence/collection (whichever is technically correct) 'iterable' and returns them in groups of 'size'.

    Example
        If we want the letters of the alphabet, but in groups of 3 and no padding...
        print(groups('abcdefghijklmnopqrstuvwxyz', 3))
        # [('a', 'b', 'c'), ('d', 'e', 'f'), ..., ('v', 'w', 'x'), ('y', 'z')]

    For the iterator/generator equivalent, use 'hackytools.iterators.groups'
    """
    total = math.ceil(len(iterable) / size)
    new = [tuple(iterable[i*size:i*size+size]) for i in range(total)]
    rem = size - len(new[-1])
    if fill is True:
        if rem > 0:
            new[-1].extend([fill_value] * rem)
    return new


# Marked for review & possible removal?
def is_prime(number: int) -> bool:
    """Check if a number is prime or not. This is probably inefficient.

    :param number:  The number whose primality to check.
    """
    if number == 2:
        return True
    elif number < 2 or number % 2 == 0:
        return False
    for i in range(3, int(number ** .5) + 1, 2):
        if number % i == 0:
            return False
    return True


# Marked for review & possible relocation into `hackytools.iterators`
def iterdir(source):
    """Traverse a directory and its subdirectories, yielding all the same files
    and/or directories that os.walk would have. Uses recursion."""
    try:
        for item in os.scandir(source):
            if item.is_dir():
                if not item.is_symlink():
                    yield from iterdir(item)
            else:
                yield item.path
    except PermissionError:
        pass


# Marked for review. Consider renaming? And consider `hackytools.math` submodule?
def magnitude(number: int) -> int:
    """Return the magnitude of a given number. For instance, 993 has a magnitude of 4, while 7 has a magnitude of 2.

    :param number:   The number the generate the magnitude of.
    """
    return math.floor(math.log10(number)) + 1


# Marked for a review. Possibly belongs in a `hackytools.formatting` submodule?
def mktable(data, *, separator=" ", alignment="<", prefix="", suffix="", strip=False):
    """Generate tables from 2-D arrays. Row prefixes and suffixes are customizable, as are the per-column-alignments,
    the column separator, and whether to strip the trailing whitespace. The per-column-alignments can be passed as a
    list of alignments with the same number of columns as the data, a string of alignments with the same length as the
    rows of the data, or as a single character (which then applies to all columns).

    :param separator:   The separator to be used between the columns (Default: " ").
    :param alignment:   The alignment to be used for each column (Default: "<"). Valid values include: any of "<", "^",
                        ">", "left", "center", "right".
    :param prefix:      The prefix to be used for each row (Default: "").
    :param suffix:      The suffix to be used for each row (Default: "").
    :param strip:       Whether to strip the trailing whitespace in each row (Default: False)
    """
    alignments = {"left": "<", "center": "^", "right": ">"}
    if isinstance(alignment, str):
        alignment = alignments.get(alignment, alignment) * len(data[0])
    elif isinstance(alignment, (tuple, list)):
        alignment = [alignments.get(j, j) for j in alignment]
    widths = [max(len(col) for col in row) for row in zip(*data)]
    return "\n".join(f'{prefix}{separator.join(f"{row[ix]:{alignment[ix]}{widths[ix]}}" for ix in range(len(row)))}{suffix}'.rstrip(None if strip else "") for row in data)


# Possibly deserves to be in a `hackytools.math` submodule?
def n_primes(amount):
    """Return the first `amount` amount of primes.

    Uses the highly-optimized `hackytools.utils.primes_to` and a clever estimate for an upper-bound, then slices out the
    amount you requested.

    :param amount:  The amount of prime numbers to generate. Will always be the first `amount` primes.
    """
    scale = 10 if amount < 5 else int(amount / (1 / math.log(amount)) * 1.2) + 5
    return primes_to(scale)[:amount]


def odd1out(data):
    """Takes a sequence of items and returns a tuple of tuples containing the previously-unseen combination of all but
    one of the args as the second value in the tuple, and the "odd one out" of that combination as the first. This is
    most useful when you have 3 or more items and you want each item in 'data' but also the remaining items in 'data',
    as a way to "separate" each item from the rest on each iteration.

    Note: For the iterator version of this function, see "hackytools.iterators.odd1out"

    Example: `odd1out(range(3))` would give you: `((0, [1, 2]), (1, [0, 2]), (2, [0, 1]))`

    :param data:    The list/tuple/set to "separate" into tuples of `(one_item, rest_of_items)`.
    """
    return tuple(iterators.odd1out(data))


def powround(num, base=math.e):
    """A rounding mechanism that mimicks math.log. Returns whichever power of 'base' is closest to 'num'.

    :param base:    The base to use. For log2, use 2. For log10, use 10. (Default: math.e)
    """
    lo = base ** (math.ceil(math.log10(num)) - 1)
    hi = base * lo
    return lo if hi - num > num - lo else hi


def powround1p(num):
    """A rounding mechanism that mimicks math.log1p. Returns whichever power of math.e is closest to 'num' + 1."""
    return powround(num + 1, base=math.e)


def powround10(num):
    """A rounding mechanism that mimicks math.log10. Returns whichever power of 10 is closest to 'num'."""
    return powround(num, base=10)


def powround2(num):
    """A rounding mechanism that mimicks math.log2. Returns whichever power of 2 is closest to 'num'."""
    return powround(num, base=2)


# Possibly deserves to be in a `hackytools.math` submodule?
def primes_to(limit):
    """Return a numpy array of all the primes under `limit`. This function is very optimized for speed. It takes
    advantage of the SIMD-nature of array operation in `numpy`.

    :param limit:   Only generate primes up to, but not including, this number.
    """
    arr = np.ones(limit, dtype=bool)
    arr[:2],arr[4::2] = 0,0
    for i in range(3, int(limit ** .5) + 1, 2):
        for j in range(3, int(i ** .5), 2):
            if i % j == 0:
                break
        else:
            arr[i+i::i] = 0
    return np.flatnonzero(arr)


# Why doesn't `random` provide this? Does it? Maybe we need our own `hackytools.math` submodule?
def randmag(size):
    """
    Returns a random number of magnitude `size`.

    Example: `rand_mag(2)` could return any number in `range(10, 100)`.

    :param size: The magnitude of the number to generate.
    """
    return random.randrange(10 ** (size - 1), 10 ** size)


# Do we need a `hackytools.formatting` submodule? Genuinely, do we?
def rem_time(seconds, *, abbrev=False, spaced=True, separator=", "):
    data = []
    space = " " if spaced else ""
    values = (60, 60, 24, 7, 52, math.inf)
    units = ("second", "minute", "hour", "day", "week", "year") if not abbrev else "smhdwy"
    quotient = seconds
    for value, unit in zip(values, units):
        if quotient >= value:
            quotient, remainder = divmod(quotient, value)
            if remainder > 0:
                if not abbrev and remainder > 1:
                    unit += "s"
                data.append("%s%s%s" % (remainder, space, unit))
        else:
            if quotient > 0:
                if not abbrev and quotient > 1:
                    unit += "s"
                data.append("%s%s%s" % (quotient, space, unit))
                break
    return separator.join(reversed(data))


# Again, do we need our own `hackytools.math` submodule?
def splitint(number):
    """Split an integer into it's individual digits."""
    n = number
    if n == 0:
        return [0]
    d = []
    while n != 0:
        d.append(n % 10)
        n //= 10
    return d[::-1]


# Marked for review. Need confirmation that this works the same way as `os.walk`.
def walk(source):
    """A slightly leaner, but more careless, `os.walk` with the same tuple return format."""
    root = source
    files = []
    dirs = []
    try:
        for item in os.scandir(source):
            if item.is_dir():
                if not item.is_symlink():
                    dirs.append(item.name)
            else:
                files.append(item.name)
    except PermissionError:
        pass
    except OSError:
        pass

    yield (root, dirs, files)
    for sub in dirs:
        yield from walk(os.path.join(root, sub))
