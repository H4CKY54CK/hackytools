# hackytools
Hacky Tools, by Hackysack (I'll never get tired of that joke.)

# Installation
You can install this package via the command:

`pip install https://github.com/H4CKY54CK/hackytools/archive/master.zip`

# What do I get?
Quite a bit, actually. There's a decorator for measuring function runtime, pretty formatting/conversions for units of time, units of size, and the rate of size over time... Take a look at the documentation to see what we offer!

# Decorators

## `@elapsed` / `@bestof`

Two decorators made for quickly timing a function. `@elapsed` only times the function once, and `@bestof` defaults to best of 7, but you can specify any number. Here's an example of how to use them.

```
from hackytools import elapsed, bestof
import time

@elapsed
def fun1():
    time.sleep(.5)
    return

@bestof
def fun2():
    time.sleep(.25)
    return

fun1()
fun2()

# Output
# 'fun1' elapsed: 500.53 ms
# 'fun2' elapsed (best of 7): avg: 250.35 ms | best: 250.28 ms | worst: 250.63 ms
```

The timing decorator also automatically converts the time returned into a sensible unit, for optimal viewing pleasure.

**And recently, a new decorator called `perf`, which lets you specify the amount of rounds, the amount of loops per round, and even a custom string to use in place of the function name!**

```
from hackytools.timing import perf

@perf
def f():
    return
f()

# Output
# 'f': avg: 38.26 ns | best: 38.07 ns | x13 rounds, 1,000,000 loops each

@perf(loops=1000)
def f():
    return
f()

# Output
# 'f': avg: 38.79 ns | 1,000 loops

@perf(desc="definitely not f")
def f():
    return
f()

# Output
# 'definitely not f': avg: 38.45 ns | best: 38.18 ns | x13 rounds, 1,000,000 loops each
```

# Notes
This package is currently being overhauled, documentation is being rewritten (or just written, since it wasn't before), and optimizations are being made. Check back soon!
