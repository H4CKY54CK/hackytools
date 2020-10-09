from functools import wraps
import time
import sys
sprint = sys.stdout.write

def ftime(ns):
    if ns < 1000:
        return f"{ns:.2f} ns"
    elif ns < 1000000:
        return f"{ns/1000:.2f} \u00B5s"
    elif ns < 1000000000:
        return f"{ns/1000000:.2f} ms"
    else:
        return f"{ns/1000000000:.2f} s"

def timeit(arg=None, repeat=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            assert repeat > 0, "You must run this function at least once..."
            times = []
            for _ in range(repeat):
                ts = time.perf_counter_ns()
                result = func(*args, **kwargs)
                te = time.perf_counter_ns() - ts
                times.append(te)
            avg = sum(times) / repeat
            if repeat == 1:
                msg = f"{func.__name__} elapsed: {ftime(avg)}"
            elif repeat > 1:
                msg = f"{func.__name__} average elapsed: {ftime(avg)} | best (of {repeat:,}): {ftime(min(times))} | worst (of {repeat:,}): {ftime(max(times))}"
            sprint(f"{msg}\n")
            return result
        return wrapper
    if callable(arg):
        return decorator(arg)
    elif repeat == 1 and type(arg) == int:
        repeat = arg or 1
    return decorator

def timeable(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        freq = kwargs.get('_frequency', None)
        kwargs.pop('_frequency', None)
        if not freq:
            return function(*args, **kwargs)
        times = []
        for _ in range(freq):
            ts = time.perf_counter_ns()
            result = function(*args, **kwargs)
            te = time.perf_counter_ns() - ts
            times.append(te)
        avg = sum(times) / freq
        if freq == 1:
            msg = f"{function.__name__} elapsed: {ftime(avg)}"
        elif freq > 1:
            msg = f"{function.__name__} average elapsed: {ftime(avg)} | best (of {freq:,}): {ftime(min(times))} | worst (of {freq:,}): {ftime(max(times))}"
        sprint(f"{msg}\n")
        return result
    return wrapper

