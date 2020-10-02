from functools import wraps
import time
import sys
sprint = sys.stdout.write

# 100% my own code.
# Pass in nanoseconds...
def ftime(ticks, *, unit_type=True):
    units = ['ns', '\u00B5s', 'ms', 's']
    reso = [.1*10**((i*3)+1) for i in range(10)]
    q = len([i for i in reso if ticks > i])
    z = (ticks*1000)/reso[q]
    w = units[q-1]
    if unit_type:
        return f"{z:.2f} {w}"
    return z
# ... and get back an aesthetically pleasing, not-too-long
# automatically converted value, with or without a unit label.

def timeit(arg=None, repeat=1):
    def decorator(func):
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
                msg = f"`{func.__name__}` elapsed: {ftime(avg)}"
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
