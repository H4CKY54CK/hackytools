from src.hackytools.utils import *


def test_combutations():
    data = 'ABC'
    expected = tuple((('A',), ('B',), ('C',), ('A', 'B'), ('A', 'C'), ('B', 'C'), ('A', 'B', 'C')))
    assert combutations(data) == expected
    assert combutations(data, 2) == tuple(i for i in expected if len(i) <= 2)
    assert combutations(data, reverse=True) == expected[::-1]
    assert combutations(data, 2, reverse=True) == tuple(i for i in expected[::-1] if len(i) <= 2)


def test_flatten():
    data = [1, [2, [3, [[[4,5,6,7,8,9]]]]]]
    assert flatten(data) == list(range(1,10))


def test_ftime():
    data = (
        (0, '0', 'ns'),
        (10, '10', 'ns'),
        (371, '371', 'ns'),
        (5150, '5', '\u00b5s'),
        (58715, '58', '\u00b5s'),
        (987465, '987', '\u00b5s'),
        (3167431, '3', 'ms'),
        (64744741, '64', 'ms'),
        (943167497, '943', 'ms'),
        (6468541351, '6', 's'),
    )

    for n, pre, after in data:
        res = ftime(n / 1_000_000_000)
        assert res.startswith(pre), "Expected: %s | Got: %s" % (pre + ' ' + after, res)
        assert res.endswith(after), "Expected: %s | Got: %s" % (pre + ' ' + after, res)


def test_ftime_ns():
    data = (
        (0, '0', 'ns'),
        (10, '10', 'ns'),
        (371, '371', 'ns'),
        (5150, '5', '\u00b5s'),
        (58715, '58', '\u00b5s'),
        (987465, '987', '\u00b5s'),
        (3167431, '3', 'ms'),
        (64744741, '64', 'ms'),
        (943167497, '943', 'ms'),
        (6468541351, '6', 's'),
    )

    for n, pre, after in data:
        res = ftime_ns(n)
        assert res.startswith(pre), "Expected: %s | Got: %s" % (pre + ' ' + after, res)
        assert res.endswith(after), "Expected: %s | Got: %s" % (pre + ' ' + after, res)


def test_n_primes():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    assert len(n_primes(15)) == 15 and list(n_primes(15)) == primes
    for i in range(5000):
        assert len(n_primes(i)) == i


def test_primes_to():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    assert primes == list(primes_to(50))


def test_rem_time():
    data = (
        (68546438444, '1m', '8s'),
        (979779441123, '16m', '19s'),
        (7977941341123, '2h, 12m', '57s'),
        (97977941341123, '1d, 3h, 12m', '57s'),
    )

    for n, pre, after in data:
        res = rem_time(n / 1000000000, abbrev=True)
        assert res.startswith(pre), "Expected: %s | Got: %s" % (pre + ' ' + after, res)
        assert res.endswith(after), "Expected: %s | Got: %s" % (pre + ' ' + after, res)

def test_splitint():
    for i in range(1,307):
        n = 10 ** i
        nums = list(map(int,str(n)))
        assert splitint(n) == nums
