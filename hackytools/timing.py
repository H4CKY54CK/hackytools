import gc
import time
import functools
from .utils import ftime_ns
import itertools
import math


def elapsed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            old = gc.isenabled()
            gc.disable()
            ts = time.perf_counter_ns()
            result = func(*args, **kwargs)
            te = time.perf_counter_ns()
            end = te - ts
            print(f"{func.__name__!r} elapsed: {ftime_ns(end)}")
            return result
        finally:
            if old:
                gc.enable()
    return wrapper


def bestof(argument=None, loops=17):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                times = []
                old = gc.isenabled()
                gc.disable()
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
                msg = f"{func.__name__!r} stats: avg: {avg} | best: {best} | worst: {worst} | loops: {loops:,}"
                print(msg)
                return result
            finally:
                if old:
                    gc.enable()
        return wrapper
    if callable(argument):
        return decorator(argument)
    loops = argument or loops
    return decorator


def autoperf(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            timer = time.perf_counter_ns
            gcold = gc.isenabled()
            gc.disable()

            # Get an average
            ts = timer()
            func(*args, **kwargs)
            te = timer()
            dur = te - ts
            poss = 100000000 // dur
            n = 10 ** int(math.log10(poss))

            ts = timer()
            for f in itertools.repeat(func, n // 10):
                f(*args, **kwargs)
            te = timer()
            dur = (te - ts) / (n // 10)
            poss = 100000000 // dur
            n = 10 ** int(math.log10(poss))

            r = 7
            times = []
            for _ in range(r):
                ts = timer()
                for f in itertools.repeat(func, n):
                    f(*args, **kwargs)
                te = timer()
                dur = (te - ts) / n
                times.append(dur)
            best = ftime_ns(min(times))
            avg = ftime_ns(sum(times) / len(times))
            msg = f"{func.__name__!r}: best: {best} | avg: {avg} | x{r:,} rounds, {n:,} loops each"
            print(msg)
            return func(*args, **kwargs)
        finally:
            if gcold:
                gc.disable()
    return inner


def perf(arg=None, loops=None, rounds=None, *, desc=None):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                gcold = gc.isenabled()
                gc.disable()
                timer = time.perf_counter_ns

                n = loops
                r = rounds

                if loops is None:
                    ts = timer()
                    func(*args, **kwargs)
                    te = timer()
                    dur = te - ts
                    its = 100000000 // dur
                    if its == 0:
                        its = 1
                        r = 1000000000 // dur
                        if r < 10:
                            r = 1
                    n = 10 ** int(math.log10(its))

                    if its > 100:
                        ts = timer()
                        for f in itertools.repeat(func, n // 10):
                            f(*args, **kwargs)
                        te = timer()
                        dur = (te - ts) / (n // 10)
                        its = 100000000 // dur
                        n = 10 ** int(math.log10(its))

                if r is None:
                    r = 7 if loops is None else 1 if rounds is None else rounds
                name = desc or func.__name__ # dont use qualname

                # Warm up
                for f in itertools.repeat(func, n // 10):
                    f(*args, **kwargs)

                times = []
                for _ in range(r):
                    ts = timer()
                    for f in itertools.repeat(func, n):
                        f(*args, **kwargs)
                    te = timer()
                    dur = (te - ts) / n
                    times.append(dur)
                best = min(times)
                avg = sum(times) / len(times)
                msg = f"{name!r}: avg: {ftime_ns(avg)} | {n:,} loops"
                if r > 1:
                    msg = f"{name!r}: best: {ftime_ns(best)} | avg: {ftime_ns(avg)} | x{r:,} rounds, {n:,} loops each"
                print(msg)
                return func(*args, **kwargs)
            finally:
                if gcold:
                    gc.enable()
        return inner
    if callable(arg):
        return wrapper(arg)
    rounds = loops
    loops = arg
    return wrapper