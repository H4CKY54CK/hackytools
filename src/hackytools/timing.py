import gc
import time
import functools
from .utils import ftime_ns, ftime, powround10
import itertools
import math



def perf(function=None, *, loops=None, rounds=None, desc=None, timer=time.perf_counter_ns):
    """This is a decorator intended to measure the average runtime of the function it decorates. Use the keyword-only
    arguments to customize the behaviour of this tool.

    Note: This function replaces the old decorators 'elapsed' and 'bestof'.

    :param loops:   How many times iterations the function is called per round. (Default: None (automatic))
    :param rounds:  How many is called per round. (Default: 7)
    :param desc:    The text that is used as the label for the output. (Default: the decorated function's name)
    :param timer:   The timer that is used to measure the runtime. (Default: time.perf_counter_ns)
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                gcold = gc.isenabled()
                if gcold:
                    gc.disable()

                # Scope issue
                _loops = loops
                _rounds = rounds
                _desc = desc or func.__qualname__

                # Timer setup and check
                if not callable(timer):
                    raise ValueError("not a valid timer")
                _timer = timer
                # Be smart about how we determine the resolution.
                _test = _timer()
                if isinstance(_test, int):
                    _use_ns = True
                elif isinstance(_test, float):
                    _use_ns = False
                else:
                    raise ValueError("unknown timer resolution")
                _ftime = ftime_ns if _use_ns else ftime
                units = 1_000_000_000 if _use_ns else 1

                if _rounds is None:
                    _rounds = 7

                # IF AND ONLY IF the user doesn't provide the number of loops, THEN AND ONLY THEN may we determine the
                # number of loops automatically. Don't exceed 5 seconds unless the user explicitly provides the number
                # of loops. They have the ultimate say in what happens.
                if _loops is None:
                    total = 0
                    start = _timer()
                    # Run N times in a second
                    while _timer() - start <= units:
                        result = func(*args, **kwargs)
                        total += 1
                    _loops = powround10(total * 7 / _rounds)


                # Actual code
                data = []
                for r in range(_rounds):
                    start = _timer()
                    for f in itertools.repeat(func, _loops):
                        result = f(*args, **kwargs)
                    end = _timer()
                    dur = end - start
                    data.append(dur / _loops)

                avg = sum(data) / len(data)
                variance = [(avg - i) ** 2 for i in data]
                avgvar = (sum(variance) / len(variance)) ** .5

                output = "%r: avg: %s \u00b1 %s per loop | x%s rounds, x%s loops per round" % \
                    (_desc, _ftime(avg), _ftime(avgvar), format(_rounds, ","), format(_loops, ","))

                print(output)

                return result

            finally:
                if gcold:
                    gc.enable()
        return inner
    if callable(function):
        return wrapper(function)
    return wrapper
