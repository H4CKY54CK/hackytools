# hackytools
Hacky Tools, by Hackysack (I'll never get tired of that joke.)

# Installation
You can install this package via the command:

`pip install https://github.com/H4CKY54CK/hackytools/archive/master.zip`

# What do I get?
Quite a bit, actually. There's a decorator for measuring function runtime, pretty formatting/conversions for units of time, units of size, and the rate of size over time... Take a look at the documentation to see what we offer! You know, as soon as I write it up. Sorry! In the meantime, you can have a look at the source code, which is very heavily documented via docstrings!

# Decorators
## `@perf`

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
