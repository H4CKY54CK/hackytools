# hackytools
Hacky Tools, by Hackysack (I'll never get tired of that joke.)

# Installation
You can install this package via the command:

`pip install hackytools`

# What do I get?
So far, not much. But I promise that I'm working hard at gathering a bunch of my homemade tools.

For right now, you get a couple of different hacky decorators, a spritesheet/stylesheet generator (mainly for subreddit CSS), and a command line tool (currently, only a single command).

# Decorators

## `@elapsed` / `@bestof`

Two decorators made for quickly timing a function. `@elapsed` only times the function once, and `@bestof` defaults to best of 7, but you can specify any number. Here's an example of how to use them.

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

The timing decorator also automatically converts the time returned into a sensible unit, for optimal viewing pleasure.

# Command Line Commands

## `whatsmyip`

Use this at the command line to get your **public** IP address. This is just a convenience command due to me getting tired of having to specifically search "whats my ip ipv4" on Google. If I'm going to do *some* of the legwork, I may as well make it easy on myself. You can also get your **local** IP. Simply use it like:

(Example of bash prompt)

    $ whatsmyip
    $ 123.45.67.89

    $ whatsmyip local
    $ 192.168.0.69


(Example of cmd prompt)

    C:\Users\user\Desktop>whatsmyip
    $ 123.45.67.89

    C:\Users\user\Desktop>whatsmyip local
    $ 192.168.0.69

# Spritesheet/stylesheet Generation Tool

## `spriteit`

(Detailed how-to coming soon. Sorry.)

# Misc.

You also get a variety of functions to aid you in your hacky coding adventure. (Detailed documentation coming soon. Sorry!)

# More

I have more planned. I have a changelog planned, so I don't clutter the README. I have docs planned, to also avoid cluttering the README. Some of these may already be in effect. I don't know, I'm not God. Jeez. (The changelog is in effect, though.)
