from functools import wraps
import sys
import requests
import socket
import time


def ftime(ns):
    if ns < 1000:
        return f"{ns:.2f} ns"
    elif ns < 1000000:
        return f"{ns / 1000:.2f} \u00B5s"
    elif ns < 1000000000:
        return f"{ns / 1000000:.2f} ms"
    else:
        return f"{ns / 1000000000:.2f} s"


def ftime_ns(ns):
    return ftime(ns)


def elapsed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ts = time.perf_counter_ns()
        result = func(*args, **kwargs)
        te = time.perf_counter_ns() - ts
        sys.stdout.write(f"{func.__qualname__!r} elapsed: {ftime(te)}\n")
        return result
    return wrapper


def bestof(argument=None, freq=7):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            times = []
            for _ in range(freq):
                ts = time.perf_counter_ns()
                result = func(*args, **kwargs)
                te = time.perf_counter_ns() - ts
                times.append(te)

            avg = ftime(sum(times) / len(times))
            best = ftime(min(times))
            worst = ftime(max(times))

            sys.stdout.write(f"{func.__qualname__!r} elapsed (of {freq}): avg: {avg} | best: {best} | worst: {worst}\n")
            return result
        return wrapper

    if callable(argument):
        return decorator(argument)
    elif isinstance(argument, int):
        freq = argument
    return decorator


def flatten(data):
    for item in data:
        if isinstance(item, (list, tuple, set)):
            yield from flatten(item)
        else:
            yield item


def whatsmyip():
    return requests.get('https://api.ipify.org').text.strip()
