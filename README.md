# hackytools
Hacky Tools, by Hackysack (I'll never get tired of that joke.)

# Installation
You can install this package via the command:

`pip install hackytools`

To get the development version instead (where there may be unstable features) use one of the following:

`pip install https://github.com/H4CKY54CK/hackytools/archive/main.zip`  
`pip install https://github.com/H4CKY54CK/hackytools/archive/main.tar.gz`

# What do I get?
So far, not much. But I promise that I'm working hard at gathering a bunch of my homemade tools.

For right now, you get a couple of different hacky decorators, a spritesheet/stylesheet generator (mainly for subreddit CSS), and a command line tool (currently, only a single command).

# Decorators

## `@timeit`

A decorator to time how long a function takes, illustrated below.

    from hackytools import timeit
    import time

    # We need the `time` module to delay our test functions just a little bit.

    # Time how long a function takes.
    @timeit
    def main1():
        time.sleep(2)

    # Same thing, but in case you're used to using parentheses
    @timeit()
    def main2():
        time.sleep(.5)

    # Get an average elapsed time by running your function 5 times.
    @timeit(repeat=5)
    def main3():
        pass

    if __name__ == '__main__':
        main1()
        main2()
        main3()


    # main1 elapsed: 2.00 s
    # main2 elapsed: 500.38 ms
    # main3 average elapsed: 616.67 ns | best (of 5): 300.00 ns | worst (of 5): 1.90 µs

The timing decorator also automatically converts the time returned into a sensible unit, for optimal viewing pleasure.

Just be careful that you don't repeat 50 times, and your code takes 50 seconds each run. That would take forever. Be smart.

## `@timeable`

This does *nearly* the same thing as `@timeit`. However, `@timeable` by default, does **not** time your function. In fact, it doesn't interfere with it at all, unless explicitly told to do so. What do I mean? I'll explain.

    from hackytools import timeable

    @timeable
    def some_function():
        # do some stuff
        return # or whatever

    some_function()

    # Even though it is decorated, this function will act normally. However...
    # If we were to pass in a specific (unlikely to already be in use) kwargs
    # dict such as the following (and unpack it with **):

    some_function(**{'_frequency': 1})

    # some_function elapsed: 1.20 µs

    # This WILL time the function, with a frequency of 1 time(s).

    # "But that function doesn't take any arguments!", I hear you say.

    # And you'd be right. Through the magic of decorators (and some pretty basic python)
    # we can actually reach into the kwargs, get the value for this specific kwarg,
    # and then remove the kwargs from the kwargs dict. ezpz

## `@logme`

This is just a regular logging decorator. You decorate your function with `@logme`, and it logs some basic information about what just happened, to the file `{your_filename}.log`. So, if your filename was `myproject.py`, the logfile would literally be `myproject.py.log`. This is for several reasons, the most important being to not overwrite existing files. I should probably just add a file check.

    # myproject.py

    from hackytools import logme

    @logme
    def add(x, y):
        return x + y

    add(5, 6)

    # What was logged and where:
    # (DEBUG) 10/09/20 01:54:33 PM: func: add | args: (5, 6) | kwargs: {} | returned: 11
    # to file `myproject.py.log`

## `whatsmyip`

Use this at the command line to get your **public** IP address. This is just a convenience command due to me getting tired of having to specifically search "whats my ip ipv4" on Google. If I'm going to do *some* of the legwork, I may as well make it easy on myself.

# More

I have more planned. I have a changelog planned, so I don't clutter the README. I have docs planned, to also avoid cluttering the README. Some of these may already be in effect. I don't know, I'm not God. Jeez. (The changelog is in effect, though.)