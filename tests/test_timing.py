from src.hackytools.timing import *
import time

def test_perf():
    # print('@perf')
    @perf
    def f():
        return 5
    assert f() == 5

    @perf()
    def f():
        return 5
    assert f() == 5

    @perf(loops=10000)
    def f():
        return 5
    assert f() == 5

    @perf(loops=10000, rounds=7)
    def f():
        return 5
    assert f() == 5

    @perf(loops=10000, rounds=7, desc='custom desc')
    def f():
        return 5
    assert f() == 5

    @perf(loops=10000, rounds=7, desc='custom desc', timer=time.perf_counter)
    def f():
        return 5
    assert f() == 5
