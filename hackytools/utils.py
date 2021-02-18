from functools import wraps
import sys
import requests
import socket
import time
import shutil
import os
from glob import glob
from urllib.request import urlopen


def hackywalk(source):
    results = []
    paths = [source]
    while paths:
        for item in os.scandir(paths.pop(0)):
            if item.is_file():
                results.append(item.path)
            elif item.is_dir() and not item.is_symlink():
                paths.append(item.path)
            elif item.is_symlink() and not item.is_dir():
                results.append(item.path)
    return results

def icanhazip():
    return requests.get('https://ipv4.icanhazip.com').text.strip()

def ftime(ns):
    if ns < 1000:
        return f"{ns:.2f} ns"
    elif ns < 1000000:
        return f"{ns/1000:.2f} \u00B5s"
    elif ns < 1000000000:
        return f"{ns/1000000:.2f} ms"
    else:
        return f"{ns/1000000000:.2f} s"

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
            avg, best, worst = sum(times)/len(times), min(times), max(times)
            sys.stdout.write(f"{func.__qualname__!r} elapsed (best of {freq}): avg: {ftime(avg)} | best: {ftime(best)} | worst: {ftime(worst)}\n")
            return result
        return wrapper
    if callable(argument):
        return decorator(argument)
    elif isinstance(argument, int):
        freq = argument
    return decorator

def flatten(data):
    return sum(([x] if not isinstance(x, list) else flatten(x) for x in data), [])

def sprint(text):
    return sys.stdout.write(str(text))

def whatsmyip(args):
    if args.local:
        return socket.gethostbyname(socket.gethostname())
    return requests.get('https://api.ipify.org').text.strip()

# Needs testing

# @begin.start
# def wgetit(url, name=None):
#     if name is None:
#         name = os.path.split(url)[1]
#     try:
#         with open(name, 'wb') as f:
#             f.write(urlopen(url).read())
#             return f"{url} -> {name}"
#     except Exception as e:
#         return str(e)


# @begin.start
# def wcit(*filenames):

#     files = [f for g in filenames for f in glob(g)]
#     chars = 0
#     words = 0
#     lines = 0
#     system_dependent_shorthand = '\n' if os.name == 'nt' else ''
#     output = []
#     for file in files:
#         try:
#             with open(file, errors='ignore') as f:
#                 d = f.read()
#             l = len(d.split('\n'))-1
#             w = len(d.split())
#             c = os.path.getsize(file)
#             chars += c
#             words += w
#             lines += l
#             output.append((l, w, c, file))
#         except:
#             pass
#     if len(output) > 2:
#         output.append((lines, words, chars, 'total'))
#     w = max([len(str(i)) for i in (chars,words,lines)])
#     ww = max([len(str(i)) for i in (files)])
#     if w < 5:
#         w = 5
#     for item in output:
#         sys.stdout.write('{:>{width}} {:>{width}} {:>{width}} {:>{wwidth}}\n'.format(*item,width=w,wwidth=ww))

# def spout(text, pos=None):
#     if pos:
#         x,y = pos
#         return sys.stdout.write(f"\x1b[s\x1b[{x};{y}H{text}\x1b[u")
#     return sys.stdout.write(f"{text}")
