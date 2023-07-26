import gc
import time
import functools
from .utils import ftime_ns, ftime
import itertools
import math



def elapsed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            gcold = gc.isenabled()
            if gcold:
                gc.disable()
            ts = time.perf_counter_ns()
            result = func(*args, **kwargs)
            te = time.perf_counter_ns()
            end = te - ts
            print(f"{func.__qualname__!r} elapsed: {ftime_ns(end)}")
            return result
        finally:
            if gcold:
                gc.enable()
    return wrapper


def bestof(argument=None, loops=17):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                gcold = gc.isenabled()
                if gcold:
                    gc.disable()
                times = []
                for _ in range(loops + 1):
                    ts = time.perf_counter_ns()
                    result = func(*args, **kwargs)
                    te = time.perf_counter_ns()
                    end = te - ts
                    times.append(end)
                times.remove(max(times))
                avg = ftime_ns(sum(times) / len(times))
                best = ftime_ns(min(times))
                worst = ftime_ns(max(times))
                msg = f"{func.__qualname__!r} stats: avg: {avg} | best: {best} | worst: {worst} | loops: {loops:,}"
                print(msg)
                return result
            finally:
                if gcold:
                    gc.enable()
        return wrapper
    if callable(argument):
        return decorator(argument)
    loops = argument or loops
    return decorator


# # Marked for removal
# def autoperf(func):
#     @functools.wraps(func)
#     def inner(*args, **kwargs):
#         try:
#             gcold = gc.isenabled()
#             if gcold:
#                 gc.disable()
#             timer = time.perf_counter

#             # Get an average
#             ts = timer()
#             func(*args, **kwargs)
#             te = timer()
#             dur = (te - ts) * 1000000000
#             poss = 100000000 // dur
#             n = 10 ** int(math.log10(poss))

#             ts = timer()
#             for f in itertools.repeat(func, n // 10):
#                 f(*args, **kwargs)
#             te = timer()
#             dur = ((te - ts) * 1000000000) / (n // 10)
#             poss = 100000000 // dur
#             n = 10 ** int(math.log10(poss))

#             r = 7
#             times = []
#             for _ in range(r):
#                 ts = timer()
#                 for f in itertools.repeat(func, n):
#                     f(*args, **kwargs)
#                 te = timer()
#                 dur = ((te - ts) * 1000000000) / n
#                 times.append(dur)
#             best = ftime_ns(min(times))
#             avg = ftime_ns(sum(times) / len(times))
#             msg = f"{func.__qualname__!r}: avg: {avg} | best: {best} | x{r:,} rounds, {n:,} loops each"
#             print(msg)
#             return func(*args, **kwargs)
#         finally:
#             if gcold:
#                 gc.enable()
#     return inner


def perf(loops=None, rounds=None, *, desc=None):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                gcold = gc.isenabled()
                if gcold:
                    gc.disable()
                timer = time.perf_counter_ns

                _loops = loops
                _rounds = rounds

                # If no args, it's up to us to make sure we don't make the user wait too long.
                if loops is None and rounds is None:
                    # Get single run time.
                    ts = timer()
                    func(*args, **kwargs)
                    te = timer()
                    dur = te - ts
                    # Can loop roughly this many times in .1 second
                    its = 100_000_000 // dur
                    if its < 1:
                        its = 1
                    # Smooth out to a nice round power of 10
                    _loops = 10 ** int(math.log10(its))
                    _rounds = 1

                    # Try to be more accurate for faster functions
                    if its > 100:
                        subloops = _loops // 10
                        ts = timer()
                        # itertools.repeat let's us loop faster than a normal for loop
                        for f in itertools.repeat(func, subloops):
                            f(*args, **kwargs)
                        te = timer()
                        dur = te - ts
                        avg = dur / subloops
                        its = 100_000_000 // avg
                        _loops = 10 ** int(math.log10(its))
                        _rounds = min(1_000_000_000 // its, 13)
                else:
                    _rounds = rounds or 1
                    _loops = loops or 1

                # Warming up smooths out the averages
                for f in itertools.repeat(func, _loops // 10):
                    f(*args, **kwargs)

                times = []
                for _ in range(_rounds):
                    ts = timer()
                    for f in itertools.repeat(func, _loops):
                        result = f(*args, **kwargs)
                    te = timer()
                    dur = (te - ts) / _loops
                    times.append(dur)
                best = min(times)
                avg = sum(times) / len(times)

                name = desc or func.__qualname__ # dont use qualname

                msg = f"{name!r}: avg: {ftime_ns(avg)} | {_loops:,} loops"
                if _rounds > 1:
                    msg = f"{name!r}: avg: {ftime_ns(avg)} | best: {ftime_ns(best)} | x{_rounds:,} rounds, {_loops:,} loops each"
                print(msg)
                return result
            except Exception:
                raise
            finally:
                if gcold:
                    gc.enable()
        return inner
    if callable(loops):
        func = loops
        loops = None
        return wrapper(func)
    return wrapper
