from hackytools.timing import *

def test_elapsed():
    print('@elapsed')
    @elapsed
    def f():
        return 5
    assert f() == 5


def test_bestof():
    print('@bestof')
    @bestof
    def f():
        return 5
    assert f() == 5

    @bestof()
    def f():
        return 5
    assert f() == 5

    @bestof(13)
    def f():
        return 5
    assert f() == 5


def test_autoperf():
    print('@autoperf')
    @autoperf
    def f():
        return 5
    assert f() == 5


def test_perf():
    print('@perf')
    @perf
    def f():
        return 5
    assert f() == 5

    @perf()
    def f():
        return 5
    assert f() == 5

    @perf(10000)
    def f():
        return 5
    assert f() == 5

    @perf(10000, 7)
    def f():
        return 5
    assert f() == 5

    @perf(10000, 7, desc='custom desc')
    def f():
        return 5
    assert f() == 5

if __name__ == '__main__':
    test_elapsed()
    test_bestof()
    test_autoperf()
    test_perf()