# import os
import math
# import hashlib
# import random
import itertools
# import numpy as np
# import collections



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



def odd1out(data):
    """Takes a sequence of items and yields tuples containing the previously-unseen combination of all but one of the
    args as the second value in the tuple, and the "odd one out" of that combination as the first. This is most useful
    when you have 3 or more items and you want each item in 'data' but also the remaining items in 'data', as a way to
    "separate" each item from the rest on each iteration.

    Note: This is the iterator version of this function. For the regular version, see "hackytools.utils.odd1out".

    Example: 'list(odd1out(range(3)))' would give you: '[(0, [1, 2]), (1, [0, 2]), (2, [0, 1])]'

    :param data:    The list/tuple/set to "separate" into tuples of '(one_item, rest_of_items)'.
    """
    yield from ((m, tuple(i for i in data if i is not m)) for m in data)
