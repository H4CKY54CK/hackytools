import gc
import time
import sys
from functools import wraps
from .utils import ftime_ns


def elapsed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        old = gc.isenabled()
        gc.disable()
        try:
            ts = time.perf_counter_ns()
            result = func(*args, **kwargs)
            te = time.perf_counter_ns()
            end = ts - te
            sys.stdout.write(f"{func.__qualname__!r} elapsed: {ftime_ns(end)}\n")
            return result
        finally:
            if old:
                gc.enable()
    return wrapper


def bestof(argument=None, freq=7):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            times = []
            old = gc.isenabled()
            gc.disable()
            try:
                for _ in range(freq + 1):
                    ts = time.perf_counter_ns()
                    result = func(*args, **kwargs)
                    te = time.perf_counter_ns()
                    end = te - ts
                    times.append(end)
                times.remove(max(times))
                avg = ftime_ns(sum(times) / len(times))
                best = ftime_ns(min(times))
                worst = ftime_ns(max(times))
                msg = f"{func.__qualname__!r} stats: avg: {avg} | best: {best} | worst: {worst} | loops: {freq:,}\n"
                sys.stdout.write(msg)
                return result
            finally:
                if old:
                    gc.enable()
        return wrapper
    if callable(argument):
        return decorator(argument)
    freq = argument
    return decorator


def perf(argument, loops=13):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            old = gc.isenabled()
            gc.disable()
            try:
                ts = time.perf_counter_ns()
                for _ in range(loops):
                    result = func(*args, **kwargs)
                te = time.perf_counter_ns()
                avg = ftime_ns((te - ts) / loops)
                name = repr(func.__qualname__)
                msg = f"\x1b[1m{name} stats: avg: {avg} | {loops:,} loops\x1b[0m\n"
                sys.stdout.write(msg)
                return result
            finally:
                if old:
                    gc.enable()
        return wrapper
    if callable(argument):
        return decorator(argument)
    loops = argument
    return decorator
