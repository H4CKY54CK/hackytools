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

For right now, you get a function timer in the form of a decorator.

## @timeit

The timing decorator can be used in several ways, illustrated below.

    from hackytools import timeit
    import time

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
        for i in [main1, main2, main3]:
            i()


    # main1 elapsed: 2.00 s
    # main2 elapsed: 500.38 ms
    # main3 average elapsed: 616.67 ns | best (of 5): 300.00 ns | worst (of 5): 1.90 µs

The timing decorator also automatically converts the time returned into a sensible unit, for optimal viewing pleasure.

Just be careful that you don't repeat 50 times, and your code takes 50 seconds each run. That would take forever. Be smart.
