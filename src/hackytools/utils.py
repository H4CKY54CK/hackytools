import os
import math
import array
import hashlib
import random
import itertools
import numpy as np
import collections
from typing import Optional


def combutations(iterable, n=None, *, reverse=False):
    """Gives you every combination of 'iterable' for every length up to (and including) 'n'.

    For example, list(combutations("abc")) would give you:
    [('a',), ('b',), ('c',), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('a', 'b', 'c')]

    :param iterable: Iterable to use for making combutations out of.
    :param n: The max length of combinations. (Default: None)
    """
    result = tuple(item for i in range(1, (n or len(iterable)) + 1, 1) for item in itertools.combinations(iterable, i))
    if reverse:
        return result[::-1]
    return result


def file_digest(fd, algo="sha1", *, buffer=2**20):
    """Now works identically to 'hashlib.file_digest', but is available on any Python version. Hooray.

    :param fd:      The file-like object to compute the hexdigest of. Must be in binary reading mode.
    :param algo:    The algorithm used to compute the hash. Can also be a function. (Default: "sha1")
    :param buffer:  The max amount of bytes to read from the given file at once. (Default: 2**20)
    """
    m = algo() if callable(algo) else hashlib.new(algo)
    while True:
        block = fd.read(buffer)
        if not block:
            break
        m.update(block)
    return m


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
    """Flatten a list/tuple/set of any nestedness.

    :param data:    The list/tuple/set to flatten.
    """
    result = []
    for item in data:
        if isinstance(item, (tuple, list, set)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def frate(nbytes: int, seconds: int | float, *, precision: int = 2, base: int = 1024) -> str:
    """Calculate a given amount of bytes 'nbytes' transferred over elapsed time 'seconds' and
    return the result in a human-readable format.

    :param nbytes:     The amount of bytes transferred.
    :param seconds:     The elapsed time in seconds.
    :param precision:   The desired float precision of the resulting amount.
    :param base:        Which base system to use.
                        base 10 (or 1_000) uses 1_000 bytes for KB, etc.
                        base 2 (or 1024) uses 1024 bytes as KiB, etc.
                        (Default: 10)
    """
    return "%s/s" % (fsize(nbytes / seconds),)



def fsize(n: int, *, base: int = 1024, precision: int = 2):
    """Convert a file size into a human-readable format.

    :param nbytes:      The amount of bytes to convert.
    :param power:       Which base of power to use for the units. Valid values are:
                        2 or 1024 (Default): B, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB
                        10 or 1000: B, KB, MB, GB, TB, PB, EB, ZB, YB
    :param precision:   The desired precision of the resulting float. (Default: 2)
    """
    if base in (2,1024):
        base = 1024
        units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    elif base in (10,1000):
        base = 1000
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    else:
        raise ValueError("please choose between base 2 (aka 1024) and base 10 (aka 1_000)")

    for unit in units:
        if n < base:
            break
        n /= base
    return "%%.%df %s" % (precision, unit) % (n,)


# These next two functions are basically indentical, but for performance reasons they need to be explicitly defined.
def ftime(seconds: float, *, precision: int = 2, spaced: bool = True) -> str:
    """A formatting function for seconds. Customize the output with the keyword-only parameters.

    :param seconds:     The amount of seconds to convert to a human-readable format.
    :param precision:   The floating point precision to use for the output. (Default: 2)
    :param spaced:      Whether to insert a space between the number and the unit. (Default: True)
    """
    nanoseconds = seconds * 1_000_000_000
    space = " " if spaced else ""
    if nanoseconds < 1_000:
        return "%s%sns" % (format(nanoseconds, ".%df" % precision), space)
    if nanoseconds < 1_000_000:
        return "%s%s\u00b5s" % (format(nanoseconds / 1_000, ".%df" % precision), space)
    if nanoseconds < 1_000_000_000:
        return "%s%sms" % (format(nanoseconds / 1_000_000, ".%df" % precision), space)
    return "%s%ss" % (format(nanoseconds / 1_000_000_000, ".%df" % precision), space)


def ftime_ns(nanoseconds: int, *, precision: int = 2, spaced: bool = True) -> str:
    """A formatting function for nanoseconds. Customize the output with the keyword-only parameters.

    :param nanoseconds: The amount of nanoseconds to convert to a human-readable format.
    :param precision:   The floating point precision to use for the output. (Default: 2)
    :param spaced:      Whether to insert a space between the number and the unit. (Default: True)
    """
    space = " " if spaced else ""
    if nanoseconds < 1_000:
        return "%s%sns" % (format(nanoseconds, ".%df" % precision), space)
    if nanoseconds < 1_000_000:
        return "%s%s\u00b5s" % (format(nanoseconds / 1_000, ".%df" % precision), space)
    if nanoseconds < 1_000_000_000:
        return "%s%sms" % (format(nanoseconds / 1_000_000, ".%df" % precision), space)
    return "%s%ss" % (format(nanoseconds / 1_000_000_000, ".%df" % precision), space)


def groups(iterable, size: int = 2, *, fill: bool = False, fill_value: Optional = None):
    """
    Takes a sequence/collection (whichever is technically correct) 'iterable' and returns them in groups of 'size'.

    Example
        If we want the letters of the alphabet, but in groups of 3 and no padding...
        print(groups('abcdefghijklmnopqrstuvwxyz', 3))
        # [('a', 'b', 'c'), ('d', 'e', 'f'), ..., ('v', 'w', 'x'), ('y', 'z')]

    Note: For the iterator/generator equivalent, use 'hackytools.iterators.groups'.

    :param iterable:    The iterable to group into separate, smaller groups.
    :param size:        How many elements the smaller groups should contain. (Default: 2)
    :param fill:        Whether to pad the last group to 'size', should it need it. (Default: False)
    :param fill_value:  The value to pad the last group with. (Default: None)
    """
    total = math.ceil(len(iterable) / size)
    new = [tuple(iterable[i*size:i*size+size]) for i in range(total)]
    rem = size - len(new[-1])
    if fill is True:
        if rem > 0:
            new[-1].extend([fill_value] * rem)
    return new


# # Marked for review & possible relocation into `hackytools.iterators`
# def iterdir(source):
#     """Traverse a directory and its subdirectories, yielding all the same files
#     and/or directories that os.walk would have. Uses recursion."""
#     try:
#         for item in os.scandir(source):
#             if item.is_dir():
#                 if not item.is_symlink():
#                     yield from iterdir(item)
#             else:
#                 yield item.path
#     except PermissionError:
#         pass


# Marked for review. Consider renaming? And consider `hackytools.math` submodule?
def magnitude(number: int) -> int:
    """Return the magnitude of a given number. For instance, 993 has a magnitude of 4, while 7 has a magnitude of 2.

    :param number:  The number to get the magnitude of.
    """
    return math.floor(math.log10(number)) + 1


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
def n_primes(amount: int) -> array.array:
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
    return tuple((m, tuple(i for i in data if i is not m)) for m in data)


def powround(num: int | float, base: int | float = math.e) -> int | float:
    """A rounding mechanism that mimicks math.log. Returns whichever power of 'base' is closest to 'num'.

    :param base:    The base to use. For log2, use 2. For log10, use 10. (Default: math.e)
    """
    lo = base ** (math.ceil(math.log10(num)) - 1)
    hi = base * lo
    return lo if hi - num > num - lo else hi


def powround1p(num: int | float) -> int | float:
    """A rounding mechanism that mimicks math.log1p. Returns whichever power of math.e is closest to 'num' + 1.

    :param limit:   Only generate primes up to, but not including, this number.
    """
    return powround(num + 1, base=math.e)


def powround10(num: int | float) -> int | float:
    """A rounding mechanism that mimicks math.log10. Returns whichever power of 10 is closest to 'num'.

    :param limit:   Only generate primes up to, but not including, this number.
    """
    return powround(num, base=10)


def powround2(num: int | float) -> int | float:
    """A rounding mechanism that mimicks math.log2. Returns whichever power of 2 is closest to 'num'.

    :param limit:   Only generate primes up to, but not including, this number.
    """
    return powround(num, base=2)


# Possibly deserves to be in a `hackytools.math` submodule?
def primes_to(limit: int) -> array.array:
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
def rem_time(seconds, *, abbrev=False, spaced=False, separator=", "):
    """A formatting function for converting large numbers of seconds into the appropriate seconds, minutes, hours, days,
    weeks, and years. Customize the output with the keyword-only arguments.

    :param seconds:     The amount of seconds to convert.
    :param abbrev:      Whether to abbreviate the units. (Default: False)
    :param spaced:      Whether to insert a space between the value and the unit. (Default: True)
    :param separator:   The separator to use. (Default: ',')
    """
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
                data.append("%s%s%s" % (int(remainder), space, unit))
        else:
            if quotient > 0:
                if not abbrev and quotient > 1:
                    unit += "s"
                data.append("%s%s%s" % (int(quotient), space, unit))
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


# # Marked for review. Need confirmation that this works the same way as `os.walk`.
# def walk(source):
#     """A slightly leaner, but more careless, `os.walk` with the same tuple return format."""
#     root = source
#     files = []
#     dirs = []
#     try:
#         for item in os.scandir(source):
#             if item.is_dir():
#                 if not item.is_symlink():
#                     dirs.append(item.name)
#             else:
#                 files.append(item.name)
#     except PermissionError:
#         pass
#     except OSError:
#         pass

#     yield (root, dirs, files)
#     for sub in dirs:
#         yield from walk(os.path.join(root, sub))
